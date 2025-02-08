import time
import machine
import network
import espnow
from machine import I2C, Pin
from ds3231 import DS3231

# ----------------------------
# LED Setup (GPIO2 for Blinking)
# ----------------------------
led_pin = Pin(2, Pin.OUT)  # Onboard LED on GPIO2

def blink_led():
    """Blinks LED on GPIO2 to indicate data transmission."""
    led_pin.on()
    time.sleep(0.1)
    led_pin.off()

# ----------------------------
# RTC Setup (DS3231)
# ----------------------------
sda_pin = Pin(21)
scl_pin = Pin(22)
i2c = I2C(0, scl=scl_pin, sda=sda_pin)
time.sleep(0.5)
ds = DS3231(i2c)

def get_timestamp():
    """Returns a formatted timestamp [DD/MM/YYYY; HH:MM:SS] in 24-hour format."""
    rtc_time = ds.get_time()  # Get raw RTC time tuple
    if len(rtc_time) >= 6:
        year, month, day, hour, minute, second = rtc_time[:6]  # Take only first 6 values
    else:
        print("RTC Time format error, using default values")
        return "[00/00/0000; 00:00:00]"

    return f"[{day:02}/{month:02}/{year}; {hour:02}:{minute:02}:{second:02}]"

# ----------------------------
# Wi-Fi + ESP-NOW Setup
# ----------------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

esp = espnow.ESPNow()
esp.active(True)
time.sleep(0.1)

BROADCAST_MAC = b'\x3C\x8A\x1F\xA4\x8A\x9C'
esp.add_peer(BROADCAST_MAC, channel=1)  # Added channel parameter

# ----------------------------
# Parse "SET" Command (Updated for individual RPM)
# ----------------------------
def parse_set_command(cmd_str):
    """Handles setting RPM1 and RPM2 individually."""
    try:
        if not cmd_str.startswith("SET"):
            return None, None
        after_set = cmd_str[3:].strip()
        parts = after_set.split(';')

        new_rpm1 = None
        new_rpm2 = None

        for p in parts:
            sub = p.strip()
            if sub.startswith("RPM1="):
                new_rpm1 = int(sub.split("=", 1)[1])
            elif sub.startswith("RPM2="):
                new_rpm2 = int(sub.split("=", 1)[1])

        return new_rpm1, new_rpm2  # Returns None for the values not set
    except:
        return None, None

# ----------------------------
# Main Loop (Updated)
# ----------------------------
def main():
    print("ESP32 A started. Commands accepted:")
    print("  SET RPM1=<val>  | SET RPM2=<val>  | SET RPM1=<val>; RPM2=<val>\n")

    rpm1 = 0
    rpm2 = 0
    last_broadcast = time.ticks_ms()

    while True:
        # 1) Non-blocking message check
        try:
            peer, msg = esp.recv(0)
            if msg:
                cmd_str = msg.decode('utf-8').strip()
                new_rpm1, new_rpm2 = parse_set_command(cmd_str)

                if new_rpm1 is not None:
                    rpm1 = new_rpm1
                    print(f"Updated RPM1 -> {rpm1}")

                if new_rpm2 is not None:
                    rpm2 = new_rpm2
                    print(f"Updated RPM2 -> {rpm2}")
        except OSError as e:
            if e.args[0] != 110:  # 110 = ETIMEDOUT (no data)
                raise

        # 2) Broadcast every second
        if time.ticks_diff(time.ticks_ms(), last_broadcast) >= 1000:
            timestamp = get_timestamp()
            output = f"{timestamp} RPM1: {rpm1} ; RPM2: {rpm2}"
            print(output)  # Exact format preserved
            try:
                esp.send(BROADCAST_MAC, output.encode('utf-8'))
                blink_led()  # Blink LED on GPIO2 when sending data
            except OSError as e:
                print("Send error:", e)
            
            last_broadcast = time.ticks_ms()  # Reset timer

# Start program
main()
