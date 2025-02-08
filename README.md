# 🛠️ Clinostat ESP32 Communication System

A bi-directional communication system between two ESP32 devices using ESP-NOW protocol, designed for clinostat motor control with RTC time tracking.

## 🔄 System Overview

### 📡 Sender (Clinostat Controller)
- 📊 Broadcasts RPM values with timestamps every second
- 📥 Accepts commands to change RPM values
- ⏰ Integrated DS3231 RTC for precise timestamps
- 💻 Command format: `SET RPM1=<value>` or `SET RPM2=<value>` or both
- 💡 LED indicator (GPIO2):
  - 🔵 Flash: Data transmission
  - ⚫ Off: Idle state

### 🔌 Receiver (USB Bridge)
- 🖥️ Connects to computer via USB CDC
- 📤 Forwards timestamped RPM data to computer
- 📡 Relays commands from computer to sender
- 💡 LED indicator (GPIO2):
  - 🔵 Flash: Data reception
  - ⚫ Off: Idle state

## 🔧 Hardware Setup

- 2️⃣ ESP32 microcontrollers
- 2️⃣ Onboard LEDs on GPIO2
- 🕒 DS3231 RTC module (for sender)
  - SDA: GPIO21
  - SCL: GPIO22
- 🔌 USB connection for receiver

## 📡 Communication Protocol

### 📊 RPM Broadcast Format
```
[DD/MM/YYYY; HH:MM:SS] RPM1: <value> ; RPM2: <value>
```

### ⌨️ Command Format
```
SET RPM1=<value>
SET RPM2=<value>
SET RPM1=<value> ; RPM2=<value>
```
Values must be integers

## 📁 File Structure

```
clinostat-esp32-bridge/
├── clinostat/
│   ├── boot.py
│   ├── ds3231.py
│   └── code.py      # 📡 Sender with RTC implementation
├── receiver/
│   ├── boot.py
│   └── code.py      # 🔌 Receiver/bridge implementation
└── README.md        # 📖 Documentation
```

## 🚀 Installation

1. ⚡ Flash MicroPython to both ESP32s
2. 📤 Upload the corresponding code files
3. 🕒 Connect DS3231 RTC to sender ESP32
4. 🔌 Connect receiver ESP32 to computer via USB
5. ⚡ Power up sender ESP32
6. 🖥️ Monitor/send commands via serial terminal