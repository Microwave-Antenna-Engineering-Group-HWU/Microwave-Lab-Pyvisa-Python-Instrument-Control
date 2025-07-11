import pyvisa

# Initialize the resource manager
rm = pyvisa.ResourceManager()

# Open connection to the instrument
inst = rm.open_resource('USB0::0x0699::0x0353::1525069::INSTR')

# Reset the instrument to default settings (optional, good practice)
inst.write('*RST')

# Configure Channel 1 for a sine wave
inst.write('SOUR1:FUNC SIN')  # Set waveform to sine
inst.write('SOUR1:FREQ 1000')  # Set frequency to 1 kHz
inst.write('SOUR1:VOLT 2')  # Set amplitude to 2 Vpp
inst.write('SOUR1:VOLT:OFFS 0')  # Set offset to 0 V

# Enable Channel 1 output
inst.write('OUTP1 ON')

# Query the instrument to confirm settings
print("Waveform:", inst.query('SOUR1:FUNC?'))
print("Frequency:", inst.query('SOUR1:FREQ?'))
print("Amplitude:", inst.query('SOUR1:VOLT?'))
print("Offset:", inst.query('SOUR1:VOLT:OFFS?'))

# Check for errors
error = inst.query('SYST:ERR?')
print("Error Status:", error)

# Close the connection
inst.close()
rm.close()