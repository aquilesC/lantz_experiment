import importlib
import logging

import yaml

from lantz_experiment.models.actuator import Actuator
from lantz_experiment.models.device import Device
from lantz_experiment.models.sensor import Sensor

logger = logging.getLogger(__name__)


class BaseExperiment:
    _devices = None
    _sensors = None
    _actuators = None
    _props = None

    @property
    def devices(self):
        return self._devices

    @property
    def properties(self):
        return self._props

    @classmethod
    def load_devices(cls, filename):
        logger.info('Loading devices for {}'.format(cls.__name__))
        cls._devices = {}
        with open(filename) as f:
            devices = yaml.load(f)
        for dev in devices:
            logger.info('Found device: {}'.format(dev))
            if 'custom_class' in dev:
                logger.debug('{} has a custom class'.format(dev))
                custom_class = devices[dev]['custom_class'].split(':')
                dev_mod = importlib.import_module(custom_class[0])
                dev_class = getattr(dev_mod, custom_class[1])
            else:
                dev_class = Device
            logger.info('Loaded class {}'.format(dev_class))
            # dev_class._name = dev
            cls._devices[dev] = dev_class(**devices[dev])

    @classmethod
    def load_sensors(cls, filename):
        """Loads a YAML file of sensors, assuming the following structure:
        Device
          Sensor
            Properties
            ...

        """
        logger.debug('Loading Sensors for {}'.format(cls.__name__))
        cls._sensors = {}
        with open(filename) as f:
            sensors = yaml.load(f)
        for dev in sensors:
            cls._sensors[dev] = {}
            for sensor in sensors[dev]:
                logger.info('Found {} for {}'.format(sensor, dev))
                if 'custom_class' in sensor:
                    custom_class = sensors[dev]['custom_class'].split(':')
                    sen_mod = importlib.import_module(custom_class[0])
                    sen_class = getattr(sen_mod, custom_class[1])
                else:
                    sen_class = Sensor

                print(sensors[dev][sensor])
                sens = sen_class(**sensors[dev][sensor])  # Initialize the class with a dictionary of parameters
                sens.name = sensor
                print(sens._prop)
                if dev in cls._devices:
                    sens.owner = cls._devices[dev]
                else:
                    err_msg = '{} is the owner of {} but does not exist'.format(dev, sens)
                    logger.error(err_msg)
                cls._sensors[dev][sensor] = sens

    @classmethod
    def load_actuators(cls, filename):
        logger.debug('Loading Actuators for {}'.format(cls.__name__))
        cls._actuators = {}
        with open(filename) as f:
            actuators = yaml.load(f)
        for dev in actuators:
            cls._actuators[dev]= {}
            for actuator in actuators[dev]:
                logger.info('Found {} for {}'.format(actuator, dev))
                if 'custom_class' in actuator:
                    custom_class = actuators[dev]['custom_class'].split(':')
                    act_mod = importlib.import_module(custom_class[0])
                    act_class = getattr(act_mod, custom_class[1])
                else:
                    act_class = Actuator

                actu = act_class(**actuators[dev][actuator])
                actu.name = actuator
                if dev in cls._devices:
                    actu.owner = cls._devices[dev]
                else:
                    logger.error('{} is the owner of {} but does not exist'.format(dev, actu))
                cls._actuators[dev][actuator] = actu # Override the actuator parameters with the class

    def register_sensors(self):
        pass

    def initialize_devices(self):
        if self._devices is not None:
            for d in self._devices:
                d.initialize()

    def finalize_devices(self):
        if self._devices is not None:
            for d in self._devices:
                d.finalize()

    @classmethod
    def load_config(cls, filename):
        logger.debug('Loading Config from {}'.format(filename))
        with open(filename) as f:
            props = yaml.load(f)

        if 'init' in props:
            logger.debug('Init is Config File')
            if 'devices' in props['init']:
                dev_file = props['init']['devices']
                logger.info('Devices file: {}'.format(dev_file))
                cls.load_devices(dev_file)

            if 'sensors' in props['init']:
                sens_file = props['init']['sensors']
                logger.info('Sensors file: {}'.format(sens_file))
                cls.load_sensors(sens_file)

            if 'actuators' in props['init']:
                act_file = props['init']['actuators']
                logger.info('Actuators file: {}'.format(act_file))
                cls.load_actuators(act_file)

        return cls()