""" Example on defining a custom device class based on an already existent driver.
In this case the class is bound to a specific driver for an oscilloscope

"""
from numpy import mean
from examples.dummy_driver import DummyOscilloscopeDriver

from lantz_experiment.models import Device


class OscilloscopeDevice(Device):
    def __init__(self, port, **kwargs):
        super().__init__()
        self.driver = DummyOscilloscopeDriver()

    def read_sensor(self, sensor):
        # Define our own way of reading a sensor
        if 'calibration' in sensor._prop:
            # Use the calibration
            pass

        return mean(self.driver.read_values(sensor._prop['channel'], 10))