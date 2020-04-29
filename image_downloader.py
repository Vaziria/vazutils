import requests

from vazutils.ua import _random_ua
from vazutils.logger import Logger

logger = Logger(__name__)

class ImageDownloader:
	randon_ua = False

	def get_image(self, image, argreq = {}):
		# imageTokped = cloudinary.makeUrl(image)

		headers = {}
		if image.find('shopee') != -1:
			headers.update(self.shopee_header())
		else:
			headers.update(self.tokopedia_header())

		if self.randon_ua:
			headers['user-agent'] = _random_ua.get()

		# print requests.get('http://ifconfig.me/ip', proxies=proxies).text
		
		return requests.get(image, headers=headers, stream=True, timeout = 90, **argreq)


	def shopee_header(self):

		return {
			'referer': 'https://shopee.co.id/',
			'sec-fetch-dest': 'image',
			'sec-fetch-mode': 'no-cors',
			'sec-fetch-site': 'same-site',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
		}

	def tokopedia_header(self):

		return {
			'referer': 'https://www.tokopedia.com/',
			'sec-fetch-dest': 'image',
			'sec-fetch-mode': 'no-cors',
			'sec-fetch-site': 'cross-site',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
		}


if __name__ == '__main__':
	down = ImageDownloader()

	image = 'https://ecs7-p.tokopedia.net/img/cache/200-square/product-1/2019/9/23/1462197/1462197_5fe7803b-3694-4666-b3dc-77a81e83cac3_1000_1000.webp'
	down.get_image(image, gettype='tokopedia')