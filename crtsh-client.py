import json
from time import sleep
from pycrtsh import Crtsh
from loggingHelper import logger
import datetime
import configparser



messageNewCertificate = 'Domain certification created'
messageAboutToExpire = 'Domain certification about to expired'
messageExpiredCertificate = 'Domain certification expired'

config = configparser.ConfigParser()
config.read('crtsh.conf')
DAYS_BEFORE_EXPIRED = int(config.get('Config','daysBeforeExpire'))

c = Crtsh()
domains = config.get('Config','domains').split(',')

def createLog(cert, message):
    id = cert['id']
    loggedAt = cert['logged_at']
    notBefore = cert['not_before']
    notAfter = cert['not_after']
    commonName = cert['name'].replace('"','')
    issuerName = cert['ca']['name'].replace('"','')
    return f"ID=\"{id}\" Logged At=\"{loggedAt}\" Not Before=\"{notBefore}\" Not After=\"{notAfter}\" Common Name=\"{commonName}\" Issuer Name=\"{issuerName}\" Message=\"{message}\""

def sameday(date1, date2):
    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year

def expand_duplicate(c):
    """
    Separates the certificates with more than 1 domain in diferents logs.
    """
    certs = []
    for cert in c:
        for certName in cert['name'].split('\n'):
            aux = cert.copy()
            aux['name'] = certName
            certs.append(aux)
    return certs

def new_certificates_create(certs):
    """
    Checks the diff between the day before and logs any new certificate. 
    """
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterdayCerts = [cert for cert in certs if sameday(cert['logged_at'], yesterday)]
    for cert in yesterdayCerts:
        logger.info(createLog(cert, messageNewCertificate))

def certificate_expires(certs, daysBeforeExpire):
    """
    Get all the latest certificates on the list and reports the ones with more than x days.
    """
    lastestCert = []
    domains = []
    dateBeforeExpired = datetime.datetime.today() - datetime.timedelta(days=-daysBeforeExpire)
    for cert in certs:
        certName = cert['name']
        if certName not in domains:
            domains.append(certName)
            lastestCert.append(cert)      
            if datetime.datetime.today() < cert['not_after'] < dateBeforeExpired:
                logger.info(createLog(cert, messageAboutToExpire))
            if cert['not_after'] < datetime.datetime.today():
                logger.info(createLog(cert, messageExpiredCertificate))



logger.info("Starting crtsh client.")

while True:
    try:
        for domain in domains:
            certs = c.search(domain)
            certs = expand_duplicate(certs)
            new_certificates_create(certs)
            certificate_expires(certs, DAYS_BEFORE_EXPIRED)
    except Exception as e:
        print(f"[-] Error: {e}")
        
    sleep(60*60*24)

