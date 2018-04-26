""" Exemplify how to work with the Devices, Sensors and Actuators idea.
We are going to use the Tektronix TDS1012 oscilloscope as an example.
We are going to generate a second device based on a dummy driver that
does not interface with any real-world component.

"""
from lantz.drivers.tektronix import TDS1012
from examples.dummy_driver import DummyDriver

from lantz_experiment.models import Device, Sensor, Actuator


oscilloscope = Device(name='Oscilloscope')
oscilloscope.driver = TDS1012.via_serial('none')

dummy = Device(name='Dummy Device')
dummy.driver = DummyDriver()

sensor1 = Sensor(name='Sensor 1')
sensor1.owner = oscilloscope

sensor2 = Sensor(name='Sensor 2')
sensor2.owner = dummy

actuator1 = Actuator(name='Actuator 1')
actuator1.owner = dummy

print(sensor1.value)  # There is no way for the device to interpret how to read the value directly from Lantz
print(sensor2.value)  # The dummy driver answers two for anything submitted

actuator1.value = 200
print(actuator1.value)

print(dummy._sensors)
print(oscilloscope._sensors)