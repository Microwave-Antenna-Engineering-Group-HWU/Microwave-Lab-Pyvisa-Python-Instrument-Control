import pyvisa
import time

# Initialize resource manager and connect to instrument
rm = pyvisa.ResourceManager()
inst = rm.open_resource('USB0::0x0957::0x1F01::MY53271615::INSTR')
inst.timeout = 5000

# Reset instrument
inst.write("*RST")
inst.write("*CLS")

# Print instrument ID
print("Connected to: ", inst.query("*IDN?").strip())

# Frequency sweep parameters
start_freq = 800  # MHz
stop_freq = 900   # MHz
step_freq = 1     # MHz
power_level = -10 # dBm
dwell_time = 0.5  # seconds

# Perform frequency sweep
print("Starting frequency sweep...")
for freq in range(start_freq, stop_freq + 1, step_freq):
    inst.write(f"FREQ {freq}MHZ")
    inst.write(f"POW {power_level}DBM")
    inst.write("OUTP ON")
    
    # Print current settings
    current_freq = float(inst.query("FREQ?")) / 1e6
    current_power = float(inst.query("POW?"))
    output_status = inst.query("OUTP?").strip()
    print(f"Frequency: {current_freq:.1f} MHz, Power: {current_power:.1f} dBm, Output: {'ON' if output_status == '1' else 'OFF'}")
    
    time.sleep(dwell_time)

# Turn off RF output
inst.write("OUTP OFF")
print("Sweep completed, RF output turned off")

# Close connection
inst.close()
rm.close()