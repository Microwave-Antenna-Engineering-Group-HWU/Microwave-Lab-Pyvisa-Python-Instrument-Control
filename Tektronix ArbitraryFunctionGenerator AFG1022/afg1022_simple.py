"""
Author: Shayan Majumder
Email: shayan.majumder2@gmail.com

This Python script uses the PyVISA library to communicate with the Tektronix AFG1022 Arbitrary/Function Generator over USB.
It resets the instrument, configures Channel 1 to generate a 1 kHz sine wave with 2 Vpp amplitude and 0 V offset, 
and enables the output. The script then queries the configured parameters (waveform, frequency, amplitude, and offset)
and checks the system error status to verify successful configuration.

This code is the property of Heriot-Watt University and is intended strictly for research and academic use.
"""

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