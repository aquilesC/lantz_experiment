from lantz_experiment.models.device import Device


class BaseDaq(Device):
    _type = 'DAQ'
    _config = {}  # Dictionary to store common configuration values

    def set_actuator(self, actuator, value):
        pass

    def read_sensor(self, sensor):
        pass

    def analog_input_setup(self, conditions):
        pass

    def trigger_analog(self, task=None):
        pass

    def read_analog(self, task, conditions):
        pass

    def analog_output_setup(self, conditions):
        pass

    def trigger_analog_output(self, task=None):
        pass

    def is_task_complete(self, task=None):
        pass

    def stop_task(self, task=None):
        pass

    def clear_task(self, task=None):
        pass

    def __repr__(self):
        return '<Model {} for {}>'.format(self._type, self.__driver__)