from time import sleep
from pycrtsh import Crtsh
from loggingHelper import logger
import datetime

DAYS_BEFORE_EXPIRED = 20

messageNewCertificate = 'Domain certification created'
messageAboutToExpire = 'Domain certification about to expired'
messageExpiredCertificate = 'Domain certification expired'

def createLog(cert, message):
    return f"ID=\"{cert['id']}\" Logged At=\"{cert['logged_at']}\" Not Before=\"{cert['not_before']}\" Not After=\"{cert['not_after']}\" Common Name=\"{cert['name']}\" Issuer Name=\"{cert['ca']['name']}\" Message=\"{message}\""

def sameday(date1, date2):
    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year

def expand_duplicate(c):
    certs = []
    for cert in c:
        for certName in cert['name'].split('\n'):
            aux = cert.copy()
            aux['name'] = certName
            certs.append(aux)
    return certs

c = Crtsh()
domains = ['edgeuno.net', 'edgeuno.com']

logger.info("Starting crtsh client.")

while True:

    certs = c.search("edgeuno.net")
    certs = expand_duplicate(certs)

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterdayCerts = [cert for cert in certs if sameday(cert['logged_at'], yesterday)]
    for cert in yesterdayCerts:
        logger.info(createLog(cert, messageNewCertificate))

    lastestCert = []
    domains = []
    dateBeforeExpired = datetime.datetime.today() - datetime.timedelta(days=-DAYS_BEFORE_EXPIRED)
    for cert in certs:
        certName = cert['name']
        if certName not in domains:
            domains.append(certName)
            lastestCert.append(cert)      
            if datetime.datetime.today() < cert['not_after'] < dateBeforeExpired:
                logger.info(createLog(cert, messageAboutToExpire))
            if cert['not_after'] < datetime.datetime.today():
                logger.info(createLog(cert, messageExpiredCertificate))
    sleep(60*60*24)

