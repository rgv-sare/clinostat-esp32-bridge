# 🛠️ Clinostat ESP32 Communication System

A bi-directional communication system between two ESP32 devices using ESP-NOW protocol, designed for clinostat motor control.

## 🔄 System Overview

### 📡 Sender (Clinostat Controller)
- 📊 Broadcasts current RPM values every second
- 📥 Accepts commands to change RPM values
- 💻 Command format: `SET RPM1=<value> ; RPM2=<value>`
- 💡 LED indicators:
  - 🔵 Blue flash: Broadcasting RPM values
  - 🟢 Green flash: Received valid command
  - ⚫ Off: Idle state

### 🔌 Receiver (USB Bridge)
- 🖥️ Connects to computer via UART (115200 baud)
- 📤 Forwards RPM data to computer
- 📡 Relays commands from computer to sender
- 💡 LED indicators:
  - 🔵 Blue flash: Received RPM data
  - 🟢 Green flash: Valid command sent
  - 🔴 Red flash: Invalid command received
  - ⚫ Off: Idle state

## 🔧 Hardware Setup

- 2️⃣ ESP32 microcontrollers
- 2️⃣ WS2812 NeoPixel LEDs on GPIO 21
- 🔌 USB connection for receiver
- 📍 UART pins: TX(8), RX(9)

## 📡 Communication Protocol

### 📊 RPM Broadcast Format
```
RPM1: <value> ; RPM2: <value>
```

### ⌨️ Command Format
```
SET RPM1=<value> ; RPM2=<value>
```
Values must be integers between 0-255

## 📁 File Structure

```
clinostat-esp32/
├── clinostat/
│   └── code.py      # 📡 Sender implementation
├── receiver/
│   ├── boot.py      # 🔄 Startup script
│   └── code.py      # 🔌 Receiver/bridge implementation
└── README.md        # 📖 Documentation
```

## 🚀 Installation

1. ⚡ Flash MicroPython to both ESP32s
2. 📤 Upload the corresponding code files
3. 🔌 Connect receiver ESP32 to computer via USB
4. ⚡ Power up sender ESP32
5. 🖥️ Monitor/send commands via serial terminal at 115200 baud