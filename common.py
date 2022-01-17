import logging


FORMAT = '%(levelname)9s %(name)10s%(filename)16s:'\
         '%(lineno)4d -%(funcName)5s %(asctime)s, %(msecs)s, %(message)s'

logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT)

logger = logging.getLogger(__name__)