from lantz_experiment.models.daq import ModelDaq


class DummyDaq(ModelDaq):
    def idn(self):
        return '123456'

    def read_sensor(self, sensor):
        return 2

    def __repr__(self):
        return '<Model Dummy DAQ>'

    def __str__(self):
        return 'Dummy DAQ'