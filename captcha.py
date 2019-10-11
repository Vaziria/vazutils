from string import *
import random
import requests



class Decaptcha:

	username = None
	password = None

	def __init__(self, username = None, password = None):
		self.username = username
		self.password = password

	
	def acak_string(self, jum = 16):
		dit = ascii_lowercase+ascii_uppercase+digits
		
		hasil = ''
		for _ in range(0,jum):
			hasil += random.choice(dit)
		return hasil



	def decaptcha(self, img, get=False, force_input=False):
		
		if force_input or (not (self.username or self.password)):
			with open('preview.jpg', 'wb+') as out:
				out.write(img)
			
			return input('masukkan captcha : ')
		
		try:
			#set request death
			jsonConfig['captcha']
		except KeyError as e:
			logger.error('akun decapter tidak ada....')
			
			with open('preview.jpg', 'wb+') as out:
				out.write(img)
			
			return input('masukkan captcha : ')
		
		token = string.acak_string()
		header = {
			'Accept': 'application/json',
			'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary%s'%(token),
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
		}
			
		#set payload
		payload = '------WebKitFormBoundary%s'%(token)
		payload += '\r\nContent-Disposition: form-data; name="username"\r\n\r\n'+(str(self.username))

		payload += '\r\n------WebKitFormBoundary%s'%(token)
		payload += '\r\nContent-Disposition: form-data; name="password"\r\n\r\n'+(str(self.password))

		payload += '\r\n------WebKitFormBoundary%s'%(token)
		payload += '\r\nContent-Disposition: form-data; name="captchafile"; filename="preview.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'
		payload += img
		payload += '\r\n------WebKitFormBoundary%s'%(token)+'--'
		
		req = requests.post('http://api.dbcapi.me/api/captcha', headers=header, data=payload, allow_redirects=False)
		
		text = False
		for c in range(0, 30):
			tes = requests.get(req.headers['Location'], headers={'Accept': 'application/json'}).content
			logger.debug(tes)
			tes = json.loads(tes)
			if tes['text'] != '':
				text = tes['text']
				break
			time.sleep(2)
		
		return text

_decaptcha = Decaptcha()


if __name__ == '__main__':
	print(acak_string())

	# rhienata|agustine12