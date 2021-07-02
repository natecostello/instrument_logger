This is a package that implements a logging class and defines an interface for instruments that can be logged by the class.

Working idea:

`InstrumentLogger`:
- a class for logging data from instruments to a file in a csv or simlar format that we can use panda's to analyze.
- it can recieve a name that is prepended to the file it writes to, which is always named by the time/date of it when it starts logging
- it can log continuously, at a requested frequency
- it can be stopped logging continuously
- it can log on demand if not logging continuously
- it logs all data from all instruments assigned to it
- each log entry is time/date stamped
- it can be queried for its last log entry, in which case it will return a dict of all parameter measurements keyed by parameter name ~~including the timestamp for the log entry~~.

`Instrument`: 
- a thing that measures things and can be asked to provide data.  This will be an abstract interface that is implemented by things.  The interface is what logger uses.
- for each parameter it measures, it has a string name and a string unit
- it can be queried for an individual parameter measurement by that parameters's name
- it can be queried for all of its parameters at once, in which case it returns a dict of measurements key'd by the parameter name 
- when queried for a parameter it should not block, meaning it must buffer its latest value.