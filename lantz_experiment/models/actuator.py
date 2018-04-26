import logging

from .base import BaseSensorActuator


class Actuator(BaseSensorActuator):
    _type = 'actuator'

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self._prop = kwargs
        if 'name' in kwargs:
            self.name = kwargs['name']

        if 'type' in kwargs:
            self._type += ' ' + kwargs['type']

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.owner.set_actuator(self, value)