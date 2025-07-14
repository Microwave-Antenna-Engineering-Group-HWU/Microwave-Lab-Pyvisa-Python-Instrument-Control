"""
Author: Shayan Majumder
Email: shayan.majumder2@gmail.com

This Python script uses the PyVISA library to communicate with an RF signal generator over USB.
It performs basic configuration tasks such as resetting the instrument, setting the output frequency
to 850 MHz, adjusting the output power to -10 dBm, and enabling the RF output. After configuration, 
it queries and prints the instrument's identification string along with the current frequency, power, 
and output status for verification. This script is intended for use with test and measurement equipment 
in laboratory environments.

This code is the property of Heriot-Watt University and is intended for research and academic purposes.
"""
import pyvisa

# Initialize the resource manager
rm = pyvisa.ResourceManager()

# Open connection to the instrument
inst = rm.open_resource('USB0::0x0957::0x1F01::MY53271615::INSTR')

# Reset the instrument to default state
inst.write("*RST")

# Set frequency to 850 MHz
inst.write("FREQ 850MHZ")``

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