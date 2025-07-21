"""
Author: Shayan Majumder
Email: sm3054@hw.ac.uk

This Python script interfaces with a Vector Network Analyzer (VNA) using the PyVISA library to configure measurement settings,
capture spectral data, and visualize the results with matplotlib. It establishes a USB connection to an Anritsu VNA (model MS2038C),
sets a center frequency of 865 MHz, a 1 MHz span, a -21 dBm reference level, 300 Hz resolution bandwidth, and 100 Hz video bandwidth, 
with max hold and 50 averages to stabilize measurements. The script activates three markers to identify the maximum peak and 
adjacent peaks (left and right), queries their frequencies and amplitudes, and retrieves trace data. It processes the trace to estimate 
the noise floor by filtering out peaks above a 10 dB threshold from the median power and calculates the mean of remaining points. 
Finally, it plots the spectrum trace with frequency (MHz) on the x-axis and amplitude (dBm) on the y-axis, marking the peak, adjacent peaks, 
and noise floor, using numpy for numerical operations and matplotlib for visualization, with error handling for VISA and general exceptions 
to ensure robust execution and proper connection closure.

This script is designed for use in lab environments for research and academic testing involving signal generation.

This code is the property of Heriot-Watt University and is intended solely for academic and research purposes.
"""
import pyvisa
import numpy as np
import time
import matplotlib.pyplot as plt

# Initialize the resource manager
rm = pyvisa.ResourceManager()

try:
    # Open connection to the VNA Master
    inst = rm.open_resource('USB0::0x0B5B::0xFFF9::2032023_1736_30::INSTR')

    # Set timeout to 25 seconds to accommodate potential delays
    inst.timeout = 25000

    # Query the instrument ID to verify connection
    idn = inst.query('*IDN?')
    print(f"Instrument ID: {idn.strip()}")  # Expected: Anritsu,MS2038C/11,2032023,3.90

    # Configure max hold for trace 1 
    inst.write(':TRACe1:DETector MAXHold')

    # Set the center frequency to 865 MHz 
    inst.write(':SENSe:FREQuency:CENTer 865E6')
    center_freq = inst.query(':SENSe:FREQuency:CENTer?')
    print(f"Center frequency set to: {float(center_freq)/1e6} MHz")

    # Set the frequency span to 1 MHz 
    inst.write(':SENSe:FREQuency:SPAN 1E6')
    span = inst.query(':SENSe:FREQuency:SPAN?')
    print(f"Frequency span set to: {float(span)/1e6} MHz")

    # Set the amplitude reference level to -21 dBm 
    inst.write(':DISPlay:WINDow:TRACe:Y:SCALe:RLEVel -21')
    ref_level = inst.query(':DISPlay:WINDow:TRACe:Y:SCALe:RLEVel?')
    print(f"Reference level set to: {float(ref_level)} dBm")

    # Set resolution bandwidth to 300 Hz 
    inst.write(':SENSe:BANDwidth:RESolution 300')
    rbw = inst.query(':SENSe:BANDwidth:RESolution?')
    print(f"Resolution bandwidth set to: {float(rbw)} Hz")

    # Set video bandwidth to 100 Hz to match RBW 
    inst.write(':SENSe:BANDwidth:VIDeo 100')
    vbw = inst.query(':SENSe:BANDwidth:VIDeo?')
    print(f"Video bandwidth set to: {float(vbw)} Hz")

    # inst.write(':SENSe:SWEep:POINts 551')
    # points = int(inst.query(':SENSe:SWEep:POINts?'))
    # print(f"Number of trace points: {points}")
    # Enable marker 1 and set to maximum peak 
    inst.write(':CALCulate:MARKer1:STATe ON')
    inst.write(':CALCulate:MARKer1:MAXimum')

    # Enable marker 2 and set to next peak to the left 
    inst.write(':CALCulate:MARKer2:STATe ON')
    inst.write(':CALCulate:MARKer2:MAXimum:LEFT')

    # Enable marker 3 and set to next peak to the right 
    inst.write(':CALCulate:MARKer3:STATe ON')
    inst.write(':CALCulate:MARKer3:MAXimum:RIGHt')


    # Enable averaging to stabilize noise floor measurement 
    inst.write(':SENSe:AVERage:COUNt 50')  # Set 500 average
    avg_count = int(inst.query(':SENSe:AVERage:COUNt?'))
    print(f"Averaging count set to: {avg_count}")

    # Wait for a few sweeps to ensure we capture sufficient data
    print("Capturing data for 5 secs...")
    time.sleep(5)

    

    # Query the marker 1 amplitude and frequency 
    marker_data = inst.query(':CALCulate:MARKer1:Y?')
    marker_freq = inst.query(':CALCulate:MARKer1:X?')

    # Print the marker values
    print(f"Max Marker Frequency: {float(marker_freq)/1e6} MHz")
    print(f"Max Marker Amplitude: {float(marker_data)} dBm")


    # Query marker 2 amplitude and frequency 
    marker2_data = float(inst.query(':CALCulate:MARKer2:Y?'))
    marker2_freq = float(inst.query(':CALCulate:MARKer2:X?'))
    print(f"Marker 2 (Next Left) Frequency: {marker2_freq/1e6:.3f} MHz")
    print(f"Marker 2 (Next Left) Amplitude: {marker2_data:.2f} dBm")

    # Query marker 3 amplitude and frequency 
    marker3_data = float(inst.query(':CALCulate:MARKer3:Y?'))
    marker3_freq = float(inst.query(':CALCulate:MARKer3:X?'))
    print(f"Marker 3 (Next Right) Frequency: {marker3_freq/1e6:.3f} MHz")
    print(f"Marker 3 (Next Right) Amplitude: {marker3_data:.2f} dBm")


    trace_data = inst.query(':TRACe:DATA? 1')
    trace_data = trace_data.split(',')
    print(trace_data)
    trace_data[0] = trace_data[0][6:] # remove the initial # data
    print(trace_data[0])
    print(len(trace_data))

    
    trace_data_float = []

    threshold = 10  # Exclude points 10 dB above median for noise floor

    for i in range(len(trace_data)):
        try:
            trace_data_float.append(float(trace_data[i]))
        except:
            print("Courrupt string found in Index "+str(i)+" = " + trace_data[i])

    noise_floor = np.median(trace_data_float)
    trace_data_float = []
    # Assign corrupt data noise floor value
    for i in range(len(trace_data)):
        try:
            trace_data_float.append(float(trace_data[i]))
        except:
            trace_data_float.append(noise_floor)

    points = len(trace_data_float)

    # Plot the trace

    median_power = np.median(trace_data_float)
    threshold = median_power + 10  # Exclude points 10 dB above median

    noise_data = []

    for i in range(len(trace_data_float)):
        if(trace_data_float[i]<threshold):
            noise_data.append(trace_data_float[i])
        
    noise_floor = np.mean(noise_data)
    print(f"Estimated Noise Floor: {noise_floor:.2f} dBm")

    # Calculate frequency points for the x-axis
    start_freq = float(center_freq) - float(span) / 2
    stop_freq = start_freq + float(span)
    freqs = np.linspace(start_freq, stop_freq, points) / 1e6  # Convert to MHz

    # Create the plot
    plt.figure(figsize=(15, 6))
    plt.rcParams['font.family'] = 'Arial'  # Set font to Arial
    axes = plt.gca()
    axes.grid(True, which='both')  # Enable grid for major and minor ticks

    # Plot the trace with markers
    plt.plot(freqs, trace_data_float, label=f'Averaged Max Hold Trace ({int(avg_count)} iterations)', 
            linewidth=2, marker='o', markersize=6, color='black')

    # Plot max marker with red cross
    plt.plot([float(marker_freq) / 1e6], [float(marker_data)], 'r+', 
            label=f'Max Marker: {float(marker_freq)/1e6:.3f} MHz, {float(marker_data):.2f} dBm',
            markersize=15, linewidth=1.8)
    
    # Plot marker 2 (next left) with blue cross
    plt.plot([marker2_freq / 1e6], [marker2_data], 'b+', 
             label=f'Marker 2 (Left): {marker2_freq/1e6:.3f} MHz, {marker2_data:.2f} dBm',
             markersize=15, linewidth=1.8)

    # Plot marker 3 (next right) with magenta cross
    plt.plot([marker3_freq / 1e6], [marker3_data], 'm+', 
             label=f'Marker 3 (Right): {marker3_freq/1e6:.3f} MHz, {marker3_data:.2f} dBm',
             markersize=15, linewidth=1.8)


    # Plot noise floor
    plt.axhline(y=noise_floor, color='green', linestyle='--', 
                label=f'Noise Floor: {noise_floor:.2f} dBm', linewidth=1.8)

    # Set title and labels with larger font
    plt.title('Spectrum Analyzer Trace', fontsize=18, pad=15)
    plt.xlabel('Frequency (MHz)', fontsize=18)
    plt.ylabel('Amplitude (dBm)', fontsize=18)

    # Customize axis ticks (example ranges, adjust as needed)
    freq_range = stop_freq / 1e6 - start_freq / 1e6
    plt.xlim(start_freq / 1e6, stop_freq / 1e6)
    plt.xticks(np.arange(start_freq / 1e6, stop_freq / 1e6 + freq_range / 10, freq_range / 10), fontsize=18)
    plt.yticks(fontsize=18)

    # Legend
    plt.legend(loc='upper left', fontsize=18)

    # Ensure tight layout
    plt.tight_layout()

    # Show plot
    plt.show()


    

except pyvisa.errors.VisaIOError as e:
    print(f"VISA Error: {e}")
    try:
        error = inst.query(':SYSTem:ERRor?')
        print(f"System Error Status: {error.strip()}")
    except:
        print("Unable to query system error status.")
except Exception as e:
    print(f"General Error: {e}")
    try:
        error = inst.query(':SYSTem:ERRor?')
        print(f"System Error Status: {error.strip()}")
    except:
        print("Unable to query system error status.")
finally:
    # Close the instrument connection
    try:
        inst.close()
        rm.close()
    except:
        print("Error closing connection.")