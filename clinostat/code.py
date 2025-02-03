import time
import machine
import neopixel
import network
import espnow

# ----------------------------
# NeoPixel Setup (optional)
# ----------------------------
NUM_LEDS = 1
pin = machine.Pin(21)  # Adjust if needed
np = neopixel.NeoPixel(pin, NUM_LEDS)

def set_led(color):
    np[0] = color
    np.write()

# ----------------------------
# Wi-Fi + ESP-NOW Setup
# ----------------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

esp = espnow.ESPNow()
esp.active(True)
time.sleep(0.1)

BROADCAST_MAC = b'\xff\xff\xff\xff\xff\xff'
esp.add_peer(BROADCAST_MAC, channel=1)  # Added channel parameter

# ----------------------------
# Parse "SET" Command
# ----------------------------
def parse_set_command(cmd_str):
    """(Keep this function exactly as before)"""
    try:
        if not cmd_str.startswith("SET"):
            return None
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
        if (new_rpm1 is not None) and (new_rpm2 is not None):
            return (new_rpm1, new_rpm2)
        else:
            return None
    except:
        return None

# ----------------------------
# Main Loop (FIXED SYNTAX)
# ----------------------------
def main():
    set_led((0, 0, 0))
    print("ESP32 A started. It will broadcast in EXACT format:\n  RPM1: <val> ; RPM2: <val>\n")

    rpm1 = 0
    rpm2 = 0
    last_broadcast = time.ticks_ms()  # Fixed this line

    while True:
        # 1) Non-blocking message check
        try:
            peer, msg = esp.recv(0)
            if msg:
                cmd_str = msg.decode('utf-8').strip()
                parsed = parse_set_command(cmd_str)
                if parsed:
                    rpm1, rpm2 = parsed
                    print(f"Updated RPM -> RPM1={rpm1}, RPM2={rpm2}")
                    set_led((0, 255, 0))
                    time.sleep(0.2)
                    set_led((0, 0, 0))
        except OSError as e:
            if e.args[0] != 110:  # 110 = ETIMEDOUT (no data)
                raise

        # 2) Broadcast every second
        if time.ticks_diff(time.ticks_ms(), last_broadcast) >= 1000:
            output = f"RPM1: {rpm1} ; RPM2: {rpm2}"
            print(output)  # Exact format preserved
            try:
                esp.send(BROADCAST_MAC, output.encode('utf-8'))
                set_led((0, 0, 255))
                time.sleep(0.2)
                set_led((0, 0, 0))
            except OSError as e:
                print("Send error:", e)
            
            last_broadcast = time.ticks_ms()  # Reset timer

# Start program
main()
