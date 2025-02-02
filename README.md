# Clinostat ESP32 RPM Monitor

This project consists of two ESP32-based components that communicate using ESP-NOW to monitor and transmit RPM data from a clinostat's motors.

## Components

### Sender (Clinostat)
- Connected to the clinostat's motors
- Reads and transmits RPM data using ESP-NOW
- Status LED indicator:
  - Green: Sending data (0.8s)
  - Red: Idle state (0.2s)
  - Yellow: Error state (1s)

### Receiver
- USB-connected to computer
- Receives and displays RPM data
- Status LED indicator:
  - Blue flash: Data received
  - Off: Waiting for data

## Hardware Requirements

- 2x ESP32 microcontrollers
- 2x WS2812 NeoPixel LEDs (GPIO 21)
- Clinostat with dual motors
- USB cable for receiver connection

## Installation

1. Flash MicroPython to both ESP32s
2. Upload files to each device:
   - Sender: `/clinostat/code.py`
   - Receiver: `/receiver/code.py` and `/receiver/boot.py`
3. Power up both devices
4. Connect receiver to computer via USB
5. Monitor serial output (115200 baud)

## Data Format

```
RPM1: <0-255> ; RPM2: <0-255>
```

## LED Color Guide

Sender:
- 🟢 Green: Active transmission
- 🔴 Red: Idle/waiting
- 🟡 Yellow: Error state

Receiver:
- 🔵 Blue: Data received
- ⚫ Off: Standby

## File Structure

```
clinostat-esp32/
├── clinostat/
│   └── code.py      # Sender code
├── receiver/
│   ├── code.py      # Receiver code
│   └── boot.py      # Boot script
└── README.md        # This file
```