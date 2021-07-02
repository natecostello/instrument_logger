import logging
from datetime import datetime, timedelta
from time import sleep
from abc import ABC, abstractmethod
from threading import Thread

class Instrument(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def getMeasurement(self, name: str) -> str:
        """Returns the most recent measurement for 'instrument_name.parameter_name.parameter_unit"""
        pass

    @abstractmethod
    def getAllMeasurements(self) -> 'dict':
        """Returns a dict of most recent measurements keyed by 'instrument_name.parameter_name.parameter_unit'"""
        pass

    @abstractmethod
    def getParameters(self) -> 'list[str]':
        """Returns a list of parameters measured with each entry of the form 'instrument_name.parameter_name.parameter_unit'.  The elements of this list are always in the same order."""
        pass


class InstrumentLogger:

    def __init__(self):
        self._frequency = 1
        self._header = ''
        self._lastlogdict = {}
        self._lastlogentry = ''
        self._lastlogparams = []
        self._lastlogtime = ''
        self._filenameprefix = ''
        self._fileHandler = None
        self._logger = None
        self._instruments = []
        self._loggingThread = None
        self._keepLogging = False
        self._uniqueInstanceName = str(datetime.now())

        

    def __initializeLogger(self, time: str):

        # set header
        header = 'time,'
        for inst in self._instruments:
            for parameter in inst.getParameters():
                header += parameter + ','
        self._header = header[:-1]

        # set logger
        logger = logging.getLogger(self._uniqueInstanceName) 
        logger.setLevel(logging.DEBUG)
        self._logger = logger

        # set fileHandler
        filename = self._filenameprefix + '_' + time.replace(" ", "_").replace(":", "_") + ".csv"
        fh = logging.FileHandler(filename, delay=True)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        fh.setFormatter(formatter)
        self._fileHandler = fh
        self._logger.addHandler(fh)
        self._logger.info(self._header)

    def __terminateLogger(self):
        if self._logger:
            self._logger.removeHandler(self._fileHandler)
            self._logger = None
            self._fileHandler = None
            self._header = ''


    def __newLogFile(self):
        filename = self._filenameprefix + '_' + str(datetime.now).replace(" ", "_").replace(":", "_") + ".csv"
        fh = logging.FileHandler(filename, delay=True)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        fh.setFormatter(formatter)
        self._fileHandler = fh
        self._logger.addHandler(fh)
        self._logger.info(self._header)

    def __createHeader(self):
        header = 'time,'
        for inst in self._instruments:
            for parameter in inst.getParameters():
                header += parameter + ','
        self._header = header
        

    @property
    def frequency(self):
        """Get the logging frequency"""
        return self._frequency

    @frequency.setter
    def frequency(self, seconds: float):
        """Set the logging frequency"""
        self._frequency = seconds

    def __logContinuous(self):
        # TODO: think about how to keep from slowly drifting
        while self._keepLogging:
            if (datetime.now() >= self._lastlogtime + timedelta(seconds=self._frequency)):
                self.log()
            else:
                sleep(0.1)

    def start(self):
        """Start continuous logging"""
        self._keepLogging = True
        self._loggingThread = Thread(target=self.__logContinuous)
        self._loggingThread.start()

    def stop(self):
        """Stop continuous logging."""
        self._keepLogging = False

    def log(self):
        """Create a single log entry with the current instrument measurements"""

        # Check to make sure there are instruments if not, stop
        if len(self._instruments) == 0:
            self._keepLogging = False
            return
        
        self._lastlogtime = datetime.now()
        time = str(self._lastlogtime)

        # Check to make sure there is a logger initialized if not initialize
        if not self._logger:
            self.__initializeLogger(time)

        logentry = ''
        logdict = {}
        logparams = []

        logentry += time + ','
        logparams.append('time')
        logdict['time']=time

        for inst in self._instruments:
            measurements = inst.getAllMeasurements()
            parameters = inst.getParameters()
            for param in parameters:
                logentry += measurements[param] + ','
                logparams.append(param)
                logdict[param] = measurements[param]
        logentry = logentry[:-1]

        self._lastlogentry = logentry
        self._lastlogparams = logparams
        self._lastlogdict = logdict

        self._logger.info(logentry)


    def getLastLogDict(self):
        """Get a dict of all last logged values keyed by 'instrument_name.parameter_name.parameter_unit'"""
        return dict(self._lastlogdict)

    def getLastLogParams(self):
        """Get a list of all last logged params of format 'instrument_name.parameter_name.parameter_unit'"""
        return list(self._lastlogparams)

    def getLastLogEntry(self):
        """Get a string of csv values from the last log entry"""
        return self._lastlogentry

    def getHeaderString(self):
        """Get a string of csv headers of format 'instrument_name.parameter_name.parameter_unit'"""
        return self._header

    def addInstrument(self, instrument: Instrument):
        """Add an instrument to be logged.  Will stop continuous logging.  Any future logging will be written to a new file."""
        self.newLog()
        self._instruments.append(instrument)

    def newLog(self):
        """Start a new log file for next logged event.  Will stop continous logging."""
        self.stop()
        sleep(0.2)
        self.__terminateLogger()


    def setFilenamePrefix(self, prefix: str):
        """Filenames are by default named from the time of creation.  
        This adds a descriptive prefix to the file name.  Will start a new log file."""
        self._filenameprefix = prefix
        self.newLog()







