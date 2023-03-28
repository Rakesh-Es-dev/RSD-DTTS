from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
def fetch(user,password,url):
    session = Session()
    session.auth = HTTPBasicAuth(user, password)
    client = Client(wsdl=url,transport=Transport(session=session))
    return client