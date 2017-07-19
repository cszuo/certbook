import ssl, json, OpenSSL.crypto, time, gevent
from gevent import Timeout
from gevent.pool import Pool
import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()

dt = time.strftime("%Y-%m-%d")
def handle_cert(ip,cert):
	info = {}
	for i in cert.get_subject().get_components():
		if i[0] in ('CN'):
			info[i[0]] = i[1]
	res = json.dumps(info['CN']).replace('"','')
	print res
	with open('certs_%s.txt' % dt,'a+') as f:
		f.write('%s:%s\n'%(ip, res))

def getCN(ip, port):
	for i in (2,3):
		try:
			cert = ssl.get_server_certificate((ip, port), ssl_version=i) 
			x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
			handle_cert(ip, x509)
			return ;
		except Exception, e:
			if 'wrong version number' in str(e):
				continue
			else:
				print ip, e

#getCN('www.suning.com', 443)

def worker(ip, port):
	try:
		with Timeout(3):
			getCN(ip, port)
	except:
		pass

pool = Pool(100)

while True:
	try:
		ip = raw_input()
		pool.spawn(worker, ip, 443)
	except:
		break 
pool.join()



