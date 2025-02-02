import time
import random
import machine
import neopixel
import network
import espnow

# Initialize the NeoPixel on GP21
NUM_LEDS = 1  # Assuming a single WS2812 LED
pin = machine.Pin(21)  # GP21
np = neopixel.NeoPixel(pin, NUM_LEDS)

def set_led(color):
    """Set the color of the NeoPixel LED."""
    np[0] = color
    np.write()

# Initialize Wi-Fi in station mode for ESP-NOW
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESP-NOW
esp = espnow.ESPNow()  # No need to call `init()`
esp.active(True)

# Add broadcast peer (use FF:FF:FF:FF:FF:FF for broadcast)
BROADCAST_MAC = b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Broadcast MAC address
esp.add_peer(BROADCAST_MAC)

def generate_and_broadcast_rpm():
    while True:
        try:
            # Indicate output is active (green LED)
            set_led((0, 255, 0))  # Green

            # Generate random values for RPM1 and RPM2
            rpm1 = random.randint(0, 255)
            rpm2 = random.randint(0, 255)

            # Format the output
            output = f"RPM1: {rpm1} ; RPM2: {rpm2}"
            print(output)

            # Broadcast the output using ESP-NOW
            esp.send(BROADCAST_MAC, output.encode('utf-8'))

            # Keep green visible for 0.8 seconds
            time.sleep(0.8)

            # Indicate idle time (red LED)
            set_led((255, 0, 0))  # Red
            time.sleep(0.2)

        except Exception as e:
            # Indicate error with yellow LED
            set_led((255, 255, 0))  # Yellow
            print("Error broadcasting:", e)
            time.sleep(1)  # Keep yellow LED on for 1 second

# Run the function
generate_and_broadcast_rpm()

