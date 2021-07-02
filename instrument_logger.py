import logging
from abc import ABC, abstractmethod

class Instrument(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def getMeasurement(self, name: str) -> str:
        """Returns the most recent measurement for 'insturment_name.parameter_name.parameter_unit"""
        pass

    @abstractmethod
    def getAllMeasurements(self) -> 'dict':
        """Returns a dict of most recent measurements keyed by 'instrument_name.parameter_name.parameter_unit'"""
        pass

    @abstractmethod
    def getParameters(self) -> 'list[str]':
        """Returns a list of parameters measured with each entry of the form 'instrument_name.parameter_name.parameter_unit'"""
        pass


class InstrumentLogger:

    def __init__(self):
        self._frequency = 1
    
    @property
    def frequency(self):
        """Get the logging frequency"""
        return self._frequency

    @frequency.setter
    def frequency(self, seconds: float):
        """Set the logging frequency"""
        self._frequency = seconds

    def start(self):
        """Start continuous logging"""
        pass

    def stop(self):
        """Stop continuous logging"""
        pass

    def log(self):
        """Create a single log entry with the current instrument measurements"""
        pass

    def getLastLogDict(self):
        """Get a dict of all last logged values keyed by 'instrument_name.parameter_name.parameter_unit'"""
        pass

    def getLastLogEntry(self):
        """Get a string of csv values from the last log entry"""
        pass

    def getHeaderString(self):
        """Get a string of csv headers of format 'instrument_name.parameter_name.parameter_unit'"""
        pass

    def addInstrument(self, instrument: Instrument):
        """Add and instrument to be logged"""
        pass







