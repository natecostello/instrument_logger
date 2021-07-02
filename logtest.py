import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
bf = logging.Formatter('date, name, {message}',
                       style='{')
handler.setFormatter(bf)
root.addHandler(handler)
logger = logging.getLogger('foo.bar')
logger.debug('This is a DEBUG message')

logger.critical('This is a CRITICAL message')

df = logging.Formatter('$asctime $name ${levelname} $message',
                       style='$')
handler.setFormatter(df)
logger.debug('This is a DEBUG message')

logger.critical('This is a CRITICAL message')
