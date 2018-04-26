""" Exemplify how to work with the Devices, Sensors and Actuators idea.
We are going to use the Tektronix TDS1012 oscilloscope as an example.
We are going to generate a second device based on a dummy driver that
does not interface with any real-world component.

"""
from lantz.drivers.tektronix import TDS1012
from examples.dummy_driver import DummyDriver

from lantz_experiment.models import Device


oscilloscope = Device(name='Oscilloscope')
oscilloscope.driver = TDS1012.via_serial('none')

dummy = Device(name='Dummy Device')
dummy.driver = DummyDriver()

print(oscilloscope._features)
print(oscilloscope._actions)
print(oscilloscope._driver_methods)

print(dummy._features)
print(dummy._actions)
print(dummy._driver_methods)