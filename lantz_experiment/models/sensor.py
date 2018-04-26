from lantz_experiment import experiment_log as logger

from lantz_experiment.models.base import BaseSensorActuator


class Sensor(BaseSensorActuator):
    def __init__(self, **kwargs):
        type = 'sensor'
        if 'type' in kwargs:
            type = 'sensor ' + kwargs['type']
        kwargs.update({'type': type})
        super().__init__(**kwargs)
        self._prop = kwargs

    @property
    def value(self):
        logger.debug('Reading {}'.format(self))
        value = self.owner.read_sensor(self)
        logger.info('Value of {} is {}'.format(self, value))
        return value