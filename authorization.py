#coding utf8
from lxml import etree
#from io import StringIO, BytesIO
import requests

class VKAuth:

	def __init__(self,login,password,proxies):
		#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
		self.url = 'https://vk.com/'
		self.headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'keep-alive',
    'DNT':'1'
}

		self.session = requests.session()
		try:
			self.data = self.session.get(self.url, headers=self.headers,proxies = proxies)
			
		except Exception as Error:
			print(Error)
			return
		else:
			# self.data.decode = 'utf-8'
			# my_file = open("myFile.txt", "wb")
			# my_file.write(self.page)
			# my_file.close()
			parser = etree.HTMLParser(encoding='utf-8')
			self.page   = etree.parse(self.data.text, parser)
			
			#self.page = etree.fromstring(self.data.text)

			self.form = self.page.forms[0]
			self.form.fields['email'] = login
			self.form.fields['pass'] = password


		try:
			self.response = self.session.post(self.form.action, data=self.form.form_values())
		except requests.exceptions.ConnectionError as Error:
			print(Error)
			return 

	def get_response(self):
		try:
			if (self.response.status_code == requests.codes.ok):
				print(self.response.text)
			else :
				self.response.raise_for_status() 

		except	AttributeError as Error:
			print(Error)


	def get_session(self):
		try:
			return self.session
		except AttributeError as Error:
			print(Error)				

