class Procedure:
    """Normal procedure that generates a measurement in a synchronous way, for example,
    it iterates over values of actuators and reads sensors.
    """

    _sensors = {}
    _actuators = {}

    def setup(self):
        pass

    def execute(self):
        pass

    def shutdown(self):
        pass

class AsyncProcedure(Procedure):
    """Procedure that does not block during the execution. For example with a DAQ card that acquires
    data into a FIFO array. The main difference is that a separated read method has to be defined.
    """
    timer = None
    def read(self):
        pass