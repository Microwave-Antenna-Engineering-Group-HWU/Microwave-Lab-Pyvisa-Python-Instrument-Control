import pyvisa

# Initialize the resource manager
rm = pyvisa.ResourceManager()

# Open connection to the instrument
inst = rm.open_resource('USB0::0x0957::0x1F01::MY53271615::INSTR')

# Reset the instrument to default state
inst.write("*RST")

# Set frequency to 850 MHz
inst.write("FREQ 850MHZ")

# Set power level to -10 dBm
inst.write("POW -10DBM")

# Turn on RF output
inst.write("OUTP ON")

# Query and print the current settings to verify
print("Instrument ID: ", inst.query("*IDN?").strip())
print("Frequency: ", inst.query("FREQ?").strip())
print("Power: ", inst.query("POW?").strip())
print("Output Status: ", inst.query("OUTP?").strip())

# Close the connection
inst.close()
rm.close()