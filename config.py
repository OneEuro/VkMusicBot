#coding utf8

token = '595285969:AAEbBAsvpqLriHV3C9tEmLpWKsEx0uUBaHk'
database_name = './users.db'
shelve_name = 'shelve.db'
BOT_NAME = 'smartnewstest_bot'
webhook = ''
api_id = ''
api_hash = ''
phone =  '+79538700033'
vkLogin = phone
vkPassword = ''
folderMusic = r'./music/'
notDownloaded = r'./music/notdownload.txt'


API_TOKEN = ''

WEBHOOK_HOST = '127.0.0.1:5000'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '127.0.0.1:5000'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)    
