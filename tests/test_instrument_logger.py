from context import instrument_logger
from instrument_logger import Instrument, InstrumentLogger
from time import sleep
import random
import math
import os


class TestInstrument(Instrument):

    def __init__(self, name) -> None:
        self._name = name
        self.param1_name = 'param1'
        self.param1_unit = '[unit1]'
        self.param1_val = str(math.floor(random.random()*100))
        self.param2_name = 'param2'
        self.param2_unit = '[unit2]'
        self.param2_val = str(math.floor(random.random()*100))
        self.all_params = { 
            self.name + '.' + self.param1_name + '.' + self.param1_unit : str(self.param1_val),
            self.name + '.' + self.param2_name + '.' + self.param2_unit : str(self.param2_val)
        }

    @property
    def name(self):
        return self._name
    
    def getMeasurement(self, name):
        return self.all_params[name]

    def getAllMeasurements(self):
        self.param1_val = str(math.floor(random.random()*100))
        self.param2_val = str(math.floor(random.random()*100))
        self.all_params = { 
            self.name + '.' + self.param1_name + '.' + self.param1_unit : str(self.param1_val),
            self.name + '.' + self.param2_name + '.' + self.param2_unit : str(self.param2_val)
        }
        return self.all_params

    def getParameters(self):
        return list(self.all_params.keys())

print('Testing...')
os.system('rm *.csv')

print('Testing Instrument instantiation')
test_inst = TestInstrument('test_inst_1')

print('Testing getParameters')
params = test_inst.getParameters()
print(params)

print('Testing getMeasurement')
print(test_inst.getMeasurement(params[0]))

print('Testing getAllMeasurement')
print(test_inst.getAllMeasurements())

print('Testing InstrumentLogger instantiation')
test_logger = InstrumentLogger()

print('Testing addInstrument')
test_logger.addInstrument(test_inst)

print('Test adding file prefix')
test_logger.setFilenamePrefix('name')

print('Test single log')
test_logger.log()

# print('Test another single log')
# test_logger.log()

# print('Test continous for 5 seconds')
# test_logger.start()
# sleep(5)
# test_logger.stop()

# print('Test adding new file prefix while logging')
# test_logger.start()
# sleep(1)
# test_logger.setFilenamePrefix('name2')

# print('Test continous for 5 seconds')
# test_logger.start()
# sleep(5)
# test_logger.stop()

# print('Test adding a second instrument')
# test_inst2 = TestInstrument('test_inst_2')
# test_logger.addInstrument(test_inst2)

# print('Test continous for 5 seconds')
# test_logger.start()
# sleep(5)
# test_logger.stop()

# print('Test higher frequency')
# test_logger.frequency = .5

# print('Test continous for 5 seconds')
# test_logger.start()
# sleep(5)
# test_logger.stop()

print('Test logger with no instruments')

print('Testing InstrumentLogger instantiation')
test_logger = InstrumentLogger()
test_logger.setFilenamePrefix('name')
test_logger.log()