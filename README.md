
---

## 🖥️ Requirements

- Ubuntu/Linux  
- Python 3.10+  
- USB connections:
  - Table 1 → `/dev/ttyUSB0`
  - Table 2 → `/dev/ttyUSB1`  
- Motors connected and addressed via Modbus (slave IDs 1–3 per table)  

---

## ⚡ Setup Instructions

### 1. Connect the tables
```bash
ls /dev/ttyUSB*
# Expected output:
# /dev/ttyUSB0
# /dev/ttyUSB1
```

### 2. Set USB permissions
```bash
sudo chmod 666 /dev/ttyUSB0 /dev/ttyUSB1
```

### 3. Create a Python virtual environment
```bash
cd ~/MovingTable
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip3 install -r requirements.txt
```

## 🛠️ Usage Example
Run the main script:

```bash
python3 main.py
```