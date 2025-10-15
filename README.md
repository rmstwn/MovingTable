
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

