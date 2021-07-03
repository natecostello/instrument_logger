import logging
from datetime import datetime, timedelta
from time import sleep
from abc import ABC, abstractmethod
from threading import Thread

class Instrument(ABC):
    """An abstract class that provides an interface for objects to use InstrumentLogger"""

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def allmeasurements(self) -> 'dict':
        """Returns a dict of most recent measurements keyed by 'instrument_name.parameter_name.parameter_unit'"""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> 'list[str]':
        """Returns a list of parameters measured with each entry of the form 'instrument_name.parameter_name.parameter_unit'.  The elements of this list are always in the same order."""
        pass

    @abstractmethod
    def getmeasurement(self, name: str) -> str:
        """Returns the most recent measurement for 'instrument_name.parameter_name.parameter_unit"""
        pass

class InstrumentLogger:
    """A class that is assigned Instruments and timestamps and logs thier parameters to csv files."""

    def __init__(self):
        self._frequency = 1.0
        self._header = ''
        self._lastlogdict = {}
        self._lastlogentry = ''
        self._lastlogparams = []
        self._lastlogtime = ''
        self._filenameprefix = ''
        self._filehandler = None
        self._logger = None
        self._instruments = []
        self._loggingthread = None
        self._keeplogging = False
        self._unique_instance_name = str(datetime.now()) #insures this instance's logger is unique
        self._filename = ''

    def __initializelogger(self, time: str):

        # set header
        header = 'time,'
        for inst in self._instruments:
            for parameter in inst.parameters:
                header += parameter + ','
        self._header = header[:-1]

        # set logger
        logger = logging.getLogger(self._unique_instance_name) 
        logger.setLevel(logging.DEBUG)
        self._logger = logger

        # set fileHandler
        filename = self._filenameprefix + '_' + time.replace(" ", "_").replace(":", "_") + ".csv"
        fh = logging.FileHandler(filename, delay=True)
        self._filename = filename
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        fh.setFormatter(formatter)
        self._filehandler = fh
        self._logger.addHandler(fh)
        self._logger.info(self._header)

    def __terminatelogger(self):
        if self._logger:
            self._logger.removeHandler(self._filehandler)
            self._logger = None
            self._filehandler = None
            self._header = ''
            self._filename = ''

    def __logcontinuous(self):
        # TODO: think about how to keep from slowly drifting
        while self._keeplogging:
            if (datetime.now() >= self._lastlogtime + timedelta(seconds=self._frequency)):
                self.log()
            else:
                sleep(0.1)

    @property
    def frequency(self) -> float:
        """Get the logging frequency, default is 1.0"""
        return self._frequency

    @frequency.setter
    def frequency(self, seconds: float):
        """Set the logging frequency"""
        self._frequency = float(seconds)

    @property
    def lastlogdict(self) -> dict:
        """A dict of all last logged values keyed by 'instrument_name.parameter_name.parameter_unit' or empty dict"""
        return dict(self._lastlogdict)

    @property
    def lastlogparams(self) -> list:
        """A list of all last logged params of format 'instrument_name.parameter_name.parameter_unit' or empty list"""
        return list(self._lastlogparams)

    @property
    def lastlogentry(self) -> str:
        """A string of csv values from the last log entry or empty string"""
        return self._lastlogentry

    @property
    def headerstring(self):
        """Get a string of csv headers of format 'time,instrument_name.parameter_name.parameter_unit,...' or empty string"""
        return self._header

    @property
    def filenameprefix(self) -> str:
        """Get the filename prefix, default is empty string"""
        return self._filenameprefix
    
    @filenameprefix.setter
    def filenameprefix(self, prefix: str):
        """Filenames are by default named from the time of creation.  
        A prefix adds descriptive text to the filename.  Will interrupt logging and start a new log file."""
        self._filenameprefix = prefix
        self.newlog()
    
    @property
    def filename(self) -> str:
        """The filename currently in use for logging"""
        return self._filename

    def addinstrument(self, instrument: Instrument):
        """Add an instrument to be logged.  Will stop continuous logging.  
        Any future logging will be written to a new file."""
        self.newlog()
        self._instruments.append(instrument)

    def newlog(self):
        """Start a new log file for next logged event.  Will stop continous logging."""
        self.stop()
        sleep(0.2)
        self.__terminatelogger()

    def start(self):
        """Start continuous logging"""
        self._keeplogging = True
        self._loggingthread = Thread(target=self.__logcontinuous)
        self._loggingthread.start()

    def stop(self):
        """Stop continuous logging."""
        self._keeplogging = False

    def log(self):
        """Create a single log entry with the current instrument measurements"""

        # Check to make sure there are instruments if not, stop
        if len(self._instruments) == 0:
            self._keeplogging = False
            return
        
        self._lastlogtime = datetime.now()
        time = str(self._lastlogtime)

        # Check to make sure there is a logger initialized if not initialize
        if not self._logger:
            self.__initializelogger(time)

        logentry = ''
        logdict = {}
        logparams = []

        logentry += time + ','
        logparams.append('time')
        logdict['time']=time

        for inst in self._instruments:
            measurements = inst.allmeasurements
            parameters = inst.parameters
            for param in parameters:
                logentry += measurements[param] + ','
                logparams.append(param)
                logdict[param] = measurements[param]
        logentry = logentry[:-1]

        self._lastlogentry = logentry
        self._lastlogparams = logparams
        self._lastlogdict = logdict

        self._logger.info(logentry)