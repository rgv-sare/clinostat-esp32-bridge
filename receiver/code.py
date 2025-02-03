import machine
import neopixel
import network
import espnow
import time

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
# UART Setup
# ----------------------------
uart = machine.UART(0, baudrate=115200)

# ----------------------------
# Wi-Fi + ESP-NOW Setup
# ----------------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

esp = espnow.ESPNow()
esp.active(True)
BROADCAST_MAC = b'\xff\xff\xff\xff\xff\xff'
esp.add_peer(BROADCAST_MAC, channel=1)  # Critical for communication

# ----------------------------
# Command Parser (Same as ESP32 A)
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
        return (new_rpm1, new_rpm2) if (new_rpm1 and new_rpm2) else None
    except:
        return None

# ----------------------------
# Main Loop
# ----------------------------
def main():
    set_led((0, 0, 0))
    print("ESP32 B: Bridging PC commands to ESP-NOW")
    print("Send: SET RPM1=VAL ; RPM2=VAL\n")

    while True:
        try:
            # 1) Non-blocking ESP-NOW receive
            try:
                peer, msg = esp.recv(0)
                if msg:
                    print(msg.decode('utf-8'))
                    set_led((0, 0, 255))
                    time.sleep(0.1)
                    set_led((0, 0, 0))
            except OSError as e:
                if e.args[0] != 110:
                    raise

            # 2) UART handling with validation
            if uart.any():
                raw = uart.readline().decode('utf-8').strip()
                print("[PC cmd]:", raw)

                if parse_set_command(raw):
                    esp.send(BROADCAST_MAC, raw.encode('utf-8'))
                    set_led((0, 255, 0))  # Green = valid
                else:
                    print("Invalid command")
                    set_led((255, 0, 0))  # Red = invalid
                
                time.sleep(0.1)
                set_led((0, 0, 0))

        except Exception as e:
            print("Error:", e)
        
        time.sleep(0.01)

main()
