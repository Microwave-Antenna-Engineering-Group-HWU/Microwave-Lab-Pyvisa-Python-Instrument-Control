import pyvisa

def configure_afg1022(
    visa_address='USB0::0x0699::0x0353::1525069::INSTR',
    channel=1,
    waveform='SIN',
    frequency=1000,
    amplitude=2.0,
    offset=0.0,
    output_state='ON',
    reset=True
):
    """
    Configure the Tektronix AFG1022 Arbitrary/Function Generator.

    Parameters:
    - visa_address (str): VISA address of the instrument (default: 'USB0::0x0699::0x0353::1525069::INSTR').
    - channel (int): Channel to configure (1 or 2, default: 1).
    - waveform (str): Waveform type ('SIN', 'SQU', 'RAMP', 'PULS', 'NOIS', 'DC', 'ARB', or built-in waveform name).
    - frequency (float): Frequency in Hz (1 µHz to 25 MHz, depending on waveform).
    - amplitude (float): Amplitude in Vpp (1 mVpp to 10 Vpp for 50 Ω, 2 mVpp to 20 Vpp for High Z).
    - offset (float): DC offset in V (-5 V to +5 V for 50 Ω, -10 V to +10 V for High Z).
    - output_state (str): Output state ('ON' or 'OFF', default: 'ON').
    - reset (bool): Reset instrument to default settings before configuration (default: True).

    Returns:
    - dict: Configured settings and error status.
    """
    # Validate inputs
    if channel not in [1, 2]:
        raise ValueError("Channel must be 1 or 2.")
    
    valid_waveforms = ['SIN', 'SQU', 'RAMP', 'PULS', 'NOIS', 'DC', 'ARB'] 
    waveform = waveform.upper()
    if waveform not in valid_waveforms:
        raise ValueError(f"Invalid waveform. Choose from: {', '.join(valid_waveforms)}")

    # Frequency limits (in Hz)
    freq_limits = {
        'SIN': (1e-6, 25e6), 'SQU': (1e-6, 25e6), 'RAMP': (1e-6, 500e3),
        'PULS': (1e-6, 12.5e6), 'ARB': (1e-6, 10e6), 'NOIS': (None, None), 'DC': (None, None)
    }
    if waveform not in ['NOIS', 'DC'] and (frequency < freq_limits[waveform][0] or frequency > freq_limits[waveform][1]):
        raise ValueError(f"Frequency for {waveform} must be between {freq_limits[waveform][0]} Hz and {freq_limits[waveform][1]} Hz.")


    if output_state not in ['ON', 'OFF']:
        raise ValueError("Output state must be 'ON' or 'OFF'.")

    # Initialize resource manager and connect to instrument
    try:
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(visa_address)

        # Reset instrument if requested
        if reset:
            inst.write('*RST')

        # Configure channel
        ch = f'SOUR{channel}'
        inst.write(f'{ch}:FUNC {waveform}')  # Set waveform
        if waveform not in ['NOIS', 'DC']:
            inst.write(f'{ch}:FREQ {frequency}')  # Set frequency
        inst.write(f'{ch}:VOLT {amplitude}')  # Set amplitude
        inst.write(f'{ch}:VOLT:OFFS {offset}')  # Set offset
        inst.write(f'OUTP{channel} {output_state}')  # Set output state

        # Query settings to confirm
        settings = {
            'Waveform': inst.query(f'{ch}:FUNC?').strip(),
            'Frequency': inst.query(f'{ch}:FREQ?').strip() if waveform not in ['NOIS', 'DC'] else 'N/A',
            'Amplitude': inst.query(f'{ch}:VOLT?').strip(),
            'Offset': inst.query(f'{ch}:VOLT:OFFS?').strip(),
            'Output State': inst.query(f'OUTP{channel}?').strip(),
            'Error Status': inst.query('SYST:ERR?').strip()
        }

        # Close connection
        inst.close()
        rm.close()

        return settings

    except pyvisa.VisaIOError as e:
        raise Exception(f"Failed to communicate with instrument: {e}")
    except Exception as e:
        raise Exception(f"Configuration error: {e}")


settings = configure_afg1022(
    visa_address='USB0::0x0699::0x0353::1525069::INSTR',
    channel=1,
    waveform='SIN',
    frequency=100000,  # 10 kHz
    amplitude=0.15,   # 150 mVpp
    offset=0.075,     # 75 mV
    output_state='ON',
    reset=True
)
for key, value in settings.items():
    print(f"{key}: {value}")