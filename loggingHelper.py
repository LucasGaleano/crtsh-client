import logging
from logging import handlers, Formatter
from logging.handlers import SysLogHandler
from syslog import LOG_SYSLOG
import socket

log_format = f'%(asctime)s {socket.gethostname()} crtsh-client[%(process)d]: %(message)s'
log_format_syslog = 'crtsh-client[%(process)d]: %(message)s'
log_format_date = '%b %d %H:%M:%S'

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=log_format_date,
 )

handler = SysLogHandler('/dev/log',facility=LOG_SYSLOG)
handler.setFormatter(Formatter(fmt=log_format_syslog))

logger = logging.getLogger()
logger.addHandler(handler)