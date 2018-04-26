from lantz_experiment import experiment_log as logger


class BaseSensorActuator:
    """Base class to derive sensors and actuators. Both behave in the same way, the only difference is that sensors are read-only while actuators are write-only.
    A sensors is univocally defined by the pair owner/name, where the owner is a device.
    """
    def __init__(self, **kwargs):
        self._name = None
        self._type = None
        self._value = None
        self._prop = None
        self._owner = None

        if 'name' in kwargs:
            self.name = kwargs['name']

        if 'owner' in kwargs:
            self.owner = kwargs['owner']

        if 'type' in kwargs:
            self._type = kwargs['type']

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        if self._owner is not None:
            err_msg = 'Trying to change the owner of {} at runtime'.format(self.name)
            logger.error(err_msg)
            raise Exception(err_msg)

        owner.register(self)  # The sensor/actuator should be registered within the owner as well

        self._owner = owner
        logger.info('Set owner of {} as {}'.format(self, owner))


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self.name is not None:
            wrn_message = 'Trying to change an actuator name at runtime {}'.format(self.name)
            logger.warning(wrn_message)
            raise Warning(wrn_message)
        self._name = name


    def __repr__(self):
        return '<{} {}-{}>'.format(self.__class__.__name__, self.owner, self._name)

    def __str__(self):
        return '{}   {} -> {}'.format(self.__class__.__name__, self.owner, self.name)