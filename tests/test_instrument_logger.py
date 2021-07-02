from context import instrument_logger

class TestInstrument(instrument_logger.Instrument):
    name = 'testInstrument'
    param1_name = 'param1'
    param1_unit = '[unit1]'
    param1_val = str(1.001)
    param2_name = 'param2'
    param2_unit = '[unit2]'
    param2_val = str(9.999)
    all_params = { 
        name + '.' + param1_name + '.' + param1_unit : str(param1_val),
        name + '.' + param2_name + '.' + param2_unit : str(param2_val)
    }

    def getMeasurement(self, name):
        return self.all_params[name]

    def getAllMeasurements(self):
        return self.all_params

    def getParameters(self):
        return list(self.all_params.keys())

print('Testing...')
test_inst = TestInstrument()
print('Testing getParameters')
params = test_inst.getParameters()
print(params)
print('Testing getMeasurement')
print(test_inst.getMeasurement(params[0]))
print('Testing getAllMeasurement')
print(test_inst.getAllMeasurements())