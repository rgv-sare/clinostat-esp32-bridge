import machine
import network
import espnow
import time
import sys
import uselect
from machine import Pin

# ----------------------------
# LED Setup (GPIO2 for Blinking on Receive)
# ----------------------------
led_pin = machine.Pin(2, Pin.OUT)  # Onboard LED on GPIO2

def blink_led():
    """Blinks LED on GPIO2 to indicate data reception."""
    led_pin.on()
    time.sleep(0.1)
    led_pin.off()

# ----------------------------
# Wi-Fi + ESP-NOW Setup
# ----------------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

esp = espnow.ESPNow()
esp.active(True)

# Replace with the actual MAC address of the OTHER ESP32 (receiver)
SENDER_MAC = b'\x3C\x8A\x1F\xA2\x88\x38'
esp.add_peer(SENDER_MAC, channel=1)

# ----------------------------
# Command Parser (Updated)
# ----------------------------
def parse_set_command(cmd_str):
    """Parses 'SET RPM1=<val>' or 'SET RPM2=<val>' individually."""
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

        return new_rpm1, new_rpm2  # Returns None for unset values
    except:
        return None, None

# ----------------------------
# Main Loop (Updated)
# ----------------------------
def main():
    print("ESP32 B: Bridging PC commands over USB CDC to ESP-NOW")
    print("Send commands like: SET RPM1=123 or SET RPM2=456\n")

    # Create a poll object for non-blocking stdin reading
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)

    while True:
        try:
            # 1) Non-blocking ESP-NOW receive
            try:
                peer, msg = esp.recv(0)  # 0 = non-blocking
                if msg:
                    print(msg.decode('utf-8'))
                    blink_led()  # Blink LED on GPIO2 when a message is received
            except OSError as e:
                if e.args[0] != 110:  # 110 = no data
                    raise

            # 2) Non-blocking read from USB CDC (sys.stdin)
            events = poller.poll(1)  # 1 ms timeout
            if events:  
                raw = sys.stdin.readline().strip()

                if not raw:  # Ignore empty input
                    continue

                print("[PC cmd]:", raw)

                new_rpm1, new_rpm2 = parse_set_command(raw)

                if new_rpm1 is not None or new_rpm2 is not None:
                    # Forward only valid commands
                    esp.send(SENDER_MAC, raw.encode('utf-8'))
                else:
                    print("Invalid command. Use: SET RPM1=### or SET RPM2=###")
                
                time.sleep(0.1)

        except Exception as e:
            print("Error:", e)

        time.sleep(0.01)

main()

