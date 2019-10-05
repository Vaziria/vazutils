import requests
from requests import Request, Session
from requests.exceptions import RequestException
from requests import ConnectionError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .logger import Logger 

logger = Logger(__name__)

RETRY = 4


def RequestWithRetry(
    retries = 20,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def Request(method = None, *arg, **kwarg):
	
	if not method:
		return requests
	
	for c in range(RETRY):
		try:
			return getattr(requests, method)(*arg, **kwarg)
		except RequestException, e:
			logger.error(e)
			logger.info('retry..')
			
			
	
class CommonRequest(object):
	def CRequest(self, method = None, *arg, **kwarg):
		if not method:
			return self.session

		for c in range(RETRY):
			try:
				req = getattr(self.session, method)(*arg, **kwarg)
				self.save_session()
				return req
			except RequestException, e:
				logger.error(e)
				logger.info('retry..')
				
	def save_session(self):
		pass

	def create_session(self):
		self.session = Session()
				

	
class customSession(object):
	def __init__(self):
		self.session = Session()
		
	
	
	
	
	


if __name__ == '__main__':
	print Request('get', 'https://seller.shopee.co.id').text
	