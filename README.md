# Microwave Lab Python PyVISA Instrument Control

Python scripts and drivers for automating laboratory equipment in the **Microwave Lab, Heriot‑Watt University**, powered by the [PyVISA](https://pyvisa.readthedocs.io/) library.

Full list of instruments:  
🔗 https://microwaves.site.hw.ac.uk/facilities/

---

## ✅ Supported Equipment (initial)

- **Tektronix AFG1022** – Arbitrary Function Generator (example script included)
- **Keysight Agilenet N5183B** – MXG Analog Signal Generator (example script included)
- **Anritzu MS2038C** – Vector Network Analyzer and Spectrum Analyzer (example script included for Spectrum Analyzer)
- *(Planned)* Rigol DS1054Z – Oscilloscope  
- *(Planned)* Keysight 34461A – Digital Multimeter  
- *(Planned)* Aim‑TTi PL303QMD – Programmable Power Supply  

---

## 📁 Directory Layout

```
microwave-lab-pyvisa-python-instrument-control/
├── Instrument/               ← Example - Tektronix AFG1022
│   ├── datasheets/           ← PDF manuals & specs
│   └── control.py            ← Python control files example - afg1022_simple.py
├── requirements.txt          ← Python dependencies
└── README.md                 ← You’re reading it
```

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/<your-org>/microwave-lab-pyvisa-python-instrument-control.git
cd microwave-lab-pyvisa-python-instrument-control

# 2. (Optional) Virtual environment
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the example
python afg1022_simple_set_function_frequency_voltage_offset.py
```

---

## 🔧 Why PyVISA?

PyVISA abstracts communication over GPIB, USB‑TMC, TCP/IP, and serial interfaces, allowing you to:

- Send SCPI commands to instruments
- Automate measurements and data logging
- Integrate hardware control into Python test frameworks

---

## 📚 Example Usage

```python
from pyvisa import ResourceManager
import argparse

parser = argparse.ArgumentParser(description="Set Tektronix AFG1022 output frequency")
parser.add_argument("--resource", default="USB0::0x0699::0x0346::C020093::INSTR")
parser.add_argument("--frequency", type=float, required=True, help="Frequency in Hz")
args = parser.parse_args()

rm = ResourceManager()
with rm.open_resource(args.resource) as inst:
    inst.write(f"SOURce1:FREQuency {args.frequency}")
    print("Instrument ID:", inst.query("*IDN?"))
```

---

## 📚 Automation and Analytics

This code can be used to automate lab equipments and give you better insights into data visa visualization.

![Plotting Trace Data from a Spectrum Analyzer](Anritsu MS2038C Vector Network Analyzer and Spectrum Analyzer/example_trace.png)

---

## 📅 Roadmap & Contributions

- Add drivers/scripts for other lab instruments
- Auto‑discover VISA resources
- Continuous integration (GitHub Actions), unit tests, MkDocs documentation

Contributions are welcome—open an issue or pull request!

---

## 📜 License

MIT License
