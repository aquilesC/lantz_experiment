import random
from lantz import Q_


class DummyDriver:
    def idn(self):
        return 'SN: 123456'

    def set_actuator(self, actuator, value):
        return value

    def read_sensor(self, sensor):
        return 2

    def initialize(self):
        pass

    def finalize(self):
        pass


class DummyOscilloscopeDriver:
    def idn(self):
        return 'Oscilloscope 1234'

    def read_values(self, channel, num_points):
        """ Reads values from a ficticious oscilloscope.
        Returns random values in the range -10 to 10 volts.

        """

        return [random.uniform(-10, 10) for _ in range(num_points)]*Q_('V')

class DummyFunctionGenerator:
    def idn(self):
        return 'Func Gen 1234'

    def set_value(self, channel, value):
        """ Sets the value to the specified channel.
        """

        return value