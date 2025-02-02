import machine
import neopixel
import network
import espnow
import time

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
esp = espnow.ESPNow()
esp.active(True)

# Main loop to receive data
def receive_data():
    set_led((0, 0, 0))  # Ensure the LED is off initially
    print("Waiting for packets...")
    
    while True:
        try:
            # Wait for data from the sender
            peer, msg = esp.recv()
            if msg:
                # Print the received message exactly as it is
                print(msg.decode('utf-8'))
                
                # Flash the LED blue when data is received
                set_led((0, 0, 255))  # Blue
                time.sleep(0.2)  # Flash for 200ms
                set_led((0, 0, 0))  # Turn off LED

        except Exception as e:
            print("Error receiving data:", e)

# Run the function
receive_data()

