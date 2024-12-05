import pyvisa


# Function to get available devices
def list_devices():
    """
    Retrieve a list of available VISA-compatible devices connected to the system.

    Args:
        None

    Returns:
        list: A list of strings representing the available device resource names.
    """
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()


# Class to communicate with the Arduino
class ArduinoVisaDevice:
    def __init__(self, port_name):
        """
        Initialize a connection to the Arduino device at the specified port.

        Args:
            port_name (str): The VISA resource name for the Arduino device
        """
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            port_name, read_termination="\r\n", write_termination="\n"
        )

    def get_identification(self):
        """
        Retrieve the identification string from the Arduino device.

        Returns:
            str: The identification string of the device.
        """
        return self.device.query("*IDN?")

    def set_output_value(self, channel, value):
        """
        Set an output value on the specified channel.

        Args:
            channel (int): The channel number to set.
            value (int): The value to set on the specified channel, must be between 0 and 1023.
        """
        if 0 <= value <= 1023:
            self.device.query(f"OUT:CH{channel} {value}")
        else:
            raise ValueError("Value must be between 0 and 1023.")

    def get_output_value(self, channel):
        """
        Retrieve the current output value set on the specified channel.

        Args:
            channel (int): The channel number to query.

        Returns:
            int: The current output value for the specified channel (between 0 and 1023).
        """
        return int(self.device.query(f"OUT:CH{channel}?"))

    def get_input_value(self, channel):
        """
        Retrieve the raw input value of the specified channel.

        Args:
            channel (int): The channel number to query.

        Returns:
            int: The raw input value for the specified channel (between 0 and 1023).
        """
        return int(self.device.query(f"MEAS:CH{channel}?"))

    def get_input_voltage(self, channel):
        """
        Calculate and return the voltage on the specified channel based on the raw input value.

        Args:
            channel (int): The channel number to query.

        Returns:
            float: The calculated voltage on the specified channel (between 0 V and 3.3 V).
        """
        raw_value = self.get_input_value(channel)

        # Convert raw ADC value to voltage (0-1023 maps to 0-3.3V)
        voltage = (raw_value / 1023) * 3.3
        return voltage

devices=list_devices()
print(devices)

device=ArduinoVisaDevice(port_name="ASRL4::INSTR")
device.set_output_value(channel=0, value=1023)
output=device.get_output_value(channel=0)
voltage1=device.get_input_voltage(channel=1)
voltage2=device.get_input_voltage(channel=2)
print(f"output: {output}")
print(f"Gemeten op ch1: {voltage1}")
print(f"Gemeten op ch2: {voltage2}")



