import importlib
from queue import Queue
from threading import Thread

from lantz_experiment import experiment_log as logger
from lantz_experiment.models.sensor import Sensor
from lantz_experiment.models.actuator import Actuator


class Device:
    def __init__(self, **kwargs):
        logger.debug('Loading Device')
        self.__driver__ = None
        self._driver_methods = []
        self._features = []
        self._actions = []

        self._name = None
        self._type = None
        self._sensors = {}
        self._actuators = {}

        self._props = kwargs
        if 'name' in kwargs:
            self._name = kwargs['name']

    @property
    def driver(self):
        return self.__driver__

    @driver.setter
    def driver(self, driver):
        self.__driver__ = driver
        if '_lantz_anyfeat' in dir(driver):  # If this is present, we are dealing with a Lantz Driver
            self._features = [feat for feat in driver._lantz_anyfeat]
            self._actions = [action for action in driver._lantz_actions]
            self._type = 'lantz'
            self._driver_methods = []
        else:  # If there are no feats, it is not a Lantz driver
            # TODO: What happens with the methods in Lantz that are not Feats nor Actions?
            self._features = []
            self._actions = []
            self._driver_methods = \
                [func for func in dir(driver) if callable(getattr(driver, func)) and not func.startswith('_') \
                 and not func in (self._features, self._actions)]
            self._type = 'generic'

    def set_actuator(self, actuator, value):
        if actuator.name not in self._actuators:
            logger.error('The actuator {} is not registered within {}'.format(actuator, self))

        logger.debug('Trying to set {} to {}'.format(value, actuator))
        if 'set_actuator' in self._driver_methods:
            return self.driver.set_actuator(actuator, value)
        if actuator.name in self._features:
            # Setting a fake actuator through Lantz features
            setattr(self.driver, actuator.name, value)
            return getattr(self.driver, actuator.name)
        return None

    def read_sensor(self, sensor):
        if sensor.name not in self._sensors:
            logger.error('The sensor {} is not registered with {}'.format(sensor, self))

        logger.debug('Trying to read model {}'.format(self.__driver__))
        if 'read_sensor' in self._driver_methods:
            return self.driver.read_sensor(sensor)

        if sensor.name in self._features:
            # Reading a fake sensor through Lantz features
            return getattr(self.driver, sensor.name)
        return None

    def register_sensor(self, sensor):
        """

        :param sensor:
        :type sensor: Sensor
        :return:
        :rtype:
        """
        if sensor.name in self._sensors:
            logger.error('Two sensors with same name {}'.format(sensor.name))
            raise Exception('Two sensors with the same name {}'.format(sensor.name))
        self._sensors[sensor.name] = sensor

    def register_actuator(self, actuator):
        """

        :type actuator: Actuator
        """
        if actuator.name in self._actuators:
            logger.error('Two actuators with the same name {} at device {}'.format(actuator.name, self))
            raise Exception('Two actuators with the same name {}'.format(actuator.name))

        self._actuators[actuator.name] = actuator

    def register(self, periferical):
        """Register a sensor or an actuator into the device object.

        """
        if periferical._type.startswith('sensor'):
            self.register_sensor(periferical)
        elif periferical._type.startswith('actuator'):
            self.register_actuator(periferical)
        else:
            err_msg = 'A device can handle only Sensors and Actuators, not {}'.format(type(periferical))
            logger.error(err_msg)
            raise Exception(err_msg)

    def initialize(self):
        self._thread.start()
        self.__model__.initialize()

    def finalize(self):
        self._instruction_queue.put(('stop', None, None))
        self.__model__.finalize()

    def load_driver(self, driver):
        """Loads the driver into the device.

        :param driver: Driver to import into the device as package.module:class
        :type driver: Str
        """

        driver = driver.split(':')
        driver_mod = importlib.import_module(driver[0])

        driver_model = getattr(driver_mod, driver[1])
        logger.info('Loading Model {} for Device {}'.format(driver_model, self))
        self.__driver__ = driver
        logger.info('Loaded Driver {} for Device {}'.format(self.__driver__, self))

    def __repr__(self):
        return '<Device {}>'.format(self._name or self.__class__.__name__)

    def __str__(self):
        return self._name or self.__class__.__name__


class DeviceThread(Thread):
    def __init__(self, instruction_queue, results_queue):
        super().__init__()
        self.instruction_queue = instruction_queue
        self.results_queue = results_queue

    def run(self):
        while True:
            if not self.instruction_queue.empty():
                instruction, args, kwargs = self.instruction_queue.get()
                if instruction == 'stop':
                    break

                if args is None and kwargs is None:
                    res = instruction()
                elif args is None:
                    res = instruction(**kwargs)
                elif kwargs is None:
                    res = instruction(*args)
                else:
                    res = instruction(*args, **kwargs)
                self.results_queue.put(res)