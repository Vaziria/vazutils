import requests
from requests import Request, Session
from requests.exceptions import RequestException, ConnectionError
from requests import ConnectionError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .logger import Logger 
from .global_config import _config

_http_config = _config.get('http')

logger = Logger(__name__)

RETRY = 4


def get_ip(proxy = None):

	if proxy:
		return requests.get('http://ifconfig.me/ip', proxies=proxy).text
	else:
		return requests.get('http://ifconfig.me/ip').text


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
		except RequestException as e:
			logger.error(e)
			logger.info('retry..')
			
			
	
class CommonRequest:
	
	http_always_close = False

	def CRequest(self, method = None, *arg, **kwarg):

		if not method:
			return self.session

		not_save  = kwarg.get('not_save', False)
		if not_save:
			del kwarg['not_save']

		if not kwarg.get('timeout', None):
			kwarg['timeout'] = _http_config.get('timeout', 5)

		for c in range(RETRY):
			try:
				req = getattr(self.session, method)(*arg, **kwarg)
				if not not_save:
					self.save_session()

				if self.http_always_close:
					self.session.close()
					
				return req

			except ConnectionError as e:
				self.session.close()
				self.on_reset(method = method, *arg, **kwarg)


			except RequestException as e:
				self.on_connection_error()
				logger.error(e)
				logger.error(arg)
				logger.error(kwarg)
				logger.info('retry..')
				
	def on_connection_error(self):
		pass

	def save_session(self):
		pass

	def create_session(self):
		self.session = Session()
	
	def on_reset(self, method):
		logger.error('connection reset')

	
class customSession(object):
	def __init__(self):
		self.session = Session()
		
	
	
	
	
	


if __name__ == '__main__':
	print(Request('get', 'https://seller.shopee.co.id').text)
	