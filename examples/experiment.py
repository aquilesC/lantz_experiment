import logging

from lantz_experiment.experiment import BaseExperiment
from lantz_experiment import experiment_log as logger

class Experiment(BaseExperiment):
    pass

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

e = Experiment.load_config('Config/measurement_example.yml')

s = e._sensors['NI-DAQ']['Photodiode 1']
print(s.value)