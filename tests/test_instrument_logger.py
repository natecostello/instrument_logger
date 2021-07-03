from context import instrument_logger
from instrument_logger import Instrument, InstrumentLogger
from time import sleep
import random
import math
import os

import unittest


param1_name = 'param1'
param1_unit = 'unit1'
param1_val = 1.0
param2_name = 'param2'
param2_unit = 'unit2'
param2_val = 2.0
test_inst_name = 'test_inst'
all_params = {
    test_inst_name + '.' + param1_name + '.' + param1_unit : str(param1_val),
    test_inst_name + '.' + param2_name + '.' + param2_unit : str(param2_val)}

class TestInstrument(Instrument):

    def __init__(self, name):
        self._name = name
        self.param1_name = param1_name
        self.param1_unit = param1_unit
        self.param1_val = param1_val
        self.param2_name = param2_name
        self.param2_unit = param2_unit
        self.param2_val = param2_val
        self.all_params = { 
            self.name + '.' + self.param1_name + '.' + self.param1_unit : str(self.param1_val),
            self.name + '.' + self.param2_name + '.' + self.param2_unit : str(self.param2_val)
        }

    @property
    def name(self):
        return self._name
    
    def getmeasurement(self, name):
        return self.all_params[name]

    @property
    def allmeasurements(self):
        # self.param1_val = str(math.floor(random.random()*100))
        # self.param2_val = str(math.floor(random.random()*100))
        # self.all_params = { 
        #     self.name + '.' + self.param1_name + '.' + self.param1_unit : str(self.param1_val),
        #     self.name + '.' + self.param2_name + '.' + self.param2_unit : str(self.param2_val)
        # }
        return self.all_params

    @property
    def parameters(self):
        return list(self.all_params.keys())


class InstrumentTestCase(unittest.TestCase):
    def setUp(self):
        self.instrument = TestInstrument(test_inst_name)
    
    def test_instrument_name(self):
        self.assertEqual(self.instrument.name, test_inst_name)

    def test_instrument_getmeasurement(self):
        self.assertEqual(self.instrument.getmeasurement(test_inst_name + '.' + param1_name + '.' + param1_unit), str(param1_val))
    
    def test_instrument_allmeasurements(self):
        self.assertEqual(self.instrument.all_params, all_params)

class InstrumentLoggerConstructorTestCase(unittest.TestCase):
    def setUp(self):
        self.instrument = TestInstrument(test_inst_name)
        self.inst_logger = InstrumentLogger()
    
    def test_frequency_prop(self):
        self.assertEqual(self.inst_logger.frequency, 1.0)

    def test_frequency_setter(self):
        old_freq = self.inst_logger.frequency
        new_freq = 0.5
        self.inst_logger.frequency = new_freq
        self.assertEqual(self.inst_logger.frequency, new_freq)
        self.inst_logger.frequency = old_freq
    
    def test_lastlogdict(self):
        self.assertEqual(self.inst_logger.lastlogdict,{})
    
    def test_lastlogparams(self):
        self.assertEqual(self.inst_logger.lastlogparams, [])
    
    def test_lastlogentry(self):
        self.assertEqual(self.inst_logger.lastlogentry, '')
    
    def test_headerstring(self):
        self.assertEqual(self.inst_logger.headerstring, '')

    def test_filenameprefix(self):
        self.assertEqual(self.inst_logger.filenameprefix, '')
    
    def test_filenameprefix_setter(self):
        old_prefix = self.inst_logger.filenameprefix
        new_prefix = 'alajflsdfj'
        self.inst_logger.filenameprefix = new_prefix
        self.assertEqual(self.inst_logger.filenameprefix, new_prefix)
        self.inst_logger.filenameprefix = old_prefix
    
    def test_filename(self):
        self.assertEqual(self.inst_logger.filename, '')
    

    


print('Testing...')
os.system('rm *.csv')

print('Testing Instrument instantiation')
test_inst = TestInstrument('test_inst_1')

print('Testing getParameters')
params = test_inst.parameters
print(params)

print('Testing getMeasurement')
print(test_inst.getmeasurement(params[0]))

print('Testing getAllMeasurement')
print(test_inst.allmeasurements)

print('Testing InstrumentLogger instantiation')
test_logger = InstrumentLogger()

print('Testing addInstrument')
test_logger.addinstrument(test_inst)

print('Test adding file prefix')
test_logger.filenameprefix = 'name'

# print('Test single log')
# test_logger.log()

# print('Test another single log')
# test_logger.log()

print('Test continous for 5 seconds')
test_logger.start()
sleep(5)
test_logger.stop()

print('Test adding new file prefix while logging')
test_logger.start()
sleep(1)
test_logger.filenameprefix = 'name2'

print('Test continous for 5 seconds')
test_logger.start()
sleep(5)
test_logger.stop()

print('Test adding a second instrument')
test_inst2 = TestInstrument('test_inst_2')
test_logger.addinstrument(test_inst2)

print('Test continous for 5 seconds')
test_logger.start()
sleep(5)
test_logger.stop()

print('Test higher frequency')
test_logger.frequency = .5

print('Test continous for 5 seconds')
test_logger.start()
sleep(5)
test_logger.stop()

print('Test logger with no instruments')

print('Testing InstrumentLogger instantiation')
test_logger = InstrumentLogger()
test_logger.filenameprefix = 'name' 
test_logger.log()