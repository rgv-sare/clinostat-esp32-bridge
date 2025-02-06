import machine
import neopixel
import network
import espnow
import time
import sys
import uselect

# ----------------------------
# NeoPixel Setup
# ----------------------------
NUM_LEDS = 1
pin = machine.Pin(21)
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

# Replace with the actual MAC address of the OTHER ESP32 (the receiver)
SENDER_MAC = b'\xFF\xFF\xFF\xFF\xFF\xFF'
esp.add_peer(SENDER_MAC, channel=1)

# ----------------------------
# Command Parser
# ----------------------------
def parse_set_command(cmd_str):
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
        return (new_rpm1, new_rpm2) if (new_rpm1 is not None and new_rpm2 is not None) else None
    except:
        return None

def execute_command(cmd_str):
    # Simulate command execution
    print(f"Executing command: {cmd_str}")
    set_led((0, 255, 255))  # Cyan = command executed
    time.sleep(0.5)
    set_led((0, 0, 0))

# ----------------------------
# Main Loop
# ----------------------------
def main():
    set_led((0, 0, 0))
    print("ESP32 B: Bridging PC commands over USB CDC to ESP-NOW")
    print("Send commands like: SET RPM1=123 ; RPM2=456\n")

    # Create a poll object to check sys.stdin non-blocking
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)

    while True:
        try:
            # 1) Non-blocking ESP-NOW receive
            try:
                peer, msg = esp.recv(0)  # 0 = non-blocking
                if msg:
                    print(msg.decode('utf-8'))
                    set_led((0, 0, 255))  # Blue = received
                    time.sleep(0.1)
                    set_led((0, 0, 0))
            except OSError as e:
                # e.args[0] == 110 means no data was available
                if e.args[0] != 110:
                    raise

            # 2) Non-blocking read from USB CDC (sys.stdin)
            events = poller.poll(1)  # 1 ms timeout
            if events:  
                # We got data on sys.stdin
                raw = sys.stdin.readline().strip()
                print("[PC cmd]:", raw)

                if parse_set_command(raw):
                    # Forward command to the other ESP32 via ESP-NOW
                    esp.send(SENDER_MAC, raw.encode('utf-8'))
                    set_led((0, 255, 0))  # Green = valid command
                    execute_command(raw)
                else:
                    print("Invalid command. Use: SET RPM1=### ; RPM2=###")
                    set_led((255, 0, 0))  # Red = invalid
                
                time.sleep(0.1)
                set_led((0, 0, 0))

        except Exception as e:
            print("Error:", e)

        time.sleep(0.01)

main()

