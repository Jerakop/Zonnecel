import numpy as np
from Controller import ArduinoVisaDevice, list_devices

def list_available_devices():
    """
    Return a list of available devices via ArduinoVisaDevice.

    Returns:
        list: A list of device resource names.
    """
    return list_devices()


class ZonnecelExperiment:
    def __init__(self, port_name="ASRL4::INSTR", resistor_value=1.5):
        """
        Initialize the Diode Experiment with an Arduino device and a resistor value.

        Args:
            device (ArduinoVisaDevice): The Arduino device to use for controlling output and measuring input values.

            resistor_value (int): The value of the resistor (in ohms) used in the experiment.
                                            Defaults to 220 ohms.
        """
        self.resistor_value = resistor_value
        self.port_name = port_name

    def get_identification(self):
        """
        Retrieve the identification string of an Arduino device.

        Parameters:
            device_port_name (str): The name of the device's port.

        Returns:
            str: The identification string of the device, typically indicating the
                firmware or device type.

        """
        # Return the device and its identification string
        device = ArduinoVisaDevice(port_name=self.port_name)

        identification = device.get_identification()

        return device, identification

    def scan(self, n=2, start=0, stop=1023, step=1):
        """
        Scan the diode characteristics by varying the input voltage and measuring the voltage
        and current multiple times.

        Args:
            n (int): The number of measurements to take at each output value. Defaults to 5.

            start (int): The starting output value for the scan (0-1023). Defaults to 0.

            stop (int): The ending output value for the scan (0-1023). Defaults to 1023.

            step (int): The step size for output values. Defaults to 10.

        Returns:
            tuple: A tuple containing four lists:
                - voltages_mean (list): The mean voltages across the diode at each output value.

                - currents_mean (list): The mean currents through the diode at each output value.

                - voltages_std (list): The standard deviation of the voltage measurements.

                - currents_std (list): The standard deviation of the current measurements.
        """
        voltages_mean = []
        voltages_std = []
        currents_mean = []
        currents_std = []

        device, _ = self.get_identification()

        # Loop through different output values
        for output_value in range(start, stop + 1, step):
            voltages = []
            currents = []

            # Repeat measurements n times for each output value
            for _ in range(0, n):

                # Set the output value on channel 0 (input voltage)
                device.set_output_value(channel=0, value=output_value)

                # Measure the voltages at channel 1 and channel 2
                voltage_u1 = device.get_input_voltage(channel=1)
                voltage_u2 = device.get_input_voltage(channel=2)

                # Calculate the voltage across the LED and the current through it
                voltage_led = voltage_u1 - voltage_u2
                current_led = voltage_u2 / self.resistor_value

                # Store the measured values
                voltages.append(voltage_led)
                currents.append(current_led)

            # Compute the mean and standard deviation of the measurements for the current output value
            voltages_mean.append(np.mean(voltages))
            voltages_std.append(np.std(voltages) / np.sqrt(n))
            currents_mean.append(np.mean(currents))
            currents_std.append(np.std(currents) / np.sqrt(n))

            device.set_output_value(channel=0, value=0)

        return (
            np.array(voltages_mean),
            np.array(currents_mean),
            np.array(voltages_std),
            np.array(currents_std),
        )
    

experiment=ZonnecelExperiment()
scan = experiment.scan()
print(scan)
