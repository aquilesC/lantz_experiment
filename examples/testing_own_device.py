from lantz_experiment.models import Sensor

from examples.own_device import OscilloscopeDevice


oscilloscope = OscilloscopeDevice(port=1,name='oscilloscope')

sensor = Sensor(name='Sensor 1', type='analog', channel=1)
sensor.owner = oscilloscope

print(sensor.value)