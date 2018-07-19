import itertools
import requests
import string
import time
import bs4

class AAAA(object):
	# TODO: Save state as cookies and cstf_tocken

	headers = {
		'user-agent': 'my_crazy_bot',
		'cookie': 'rseor3=true; session=c6134f21077dd1669dd6e64e6453af516d5a1a7bgAJKsXFPW0dB1tPcbGCoRH1xAVUHX2NzcmZ0X3ECWCgAAAA5ZDA0NmIyZjMzYTcyMDEwMjBjNjQyMTg4MzNhZWNhNzM4Y2E1ZTYzcQNzh3EELg=='
	}
	def __init__(self):
		pass

	def get_payload(username):
		return {'csrf_token': '9d046b2f33a7201020c64218833aeca738ca5e63', 'user': username}

	def get_cookies():
		# TODO: implement this!
		pass

	def get_csrf_token():
	 	bs = bs4.BeautifulSoup(
	 		requests.get('https://www.reddit.com/register').content,
	 		'html.parser'
	 	)
	 	# TODO: Find a better way to filter csrf_token
		b = filter(lambda x: 'csrf_token' == x.attrs['name'], bs.find_all('input'))
	 	if len(b) > 1:
	 		raise ValueError("Got more than one csrf_token")

	 	return b[0].attrs['value']


r = requests.get('https://www.reddit.com/check_username')
r.cookies.set('rseor3', 'true')	
# for i in xrange(3, 10):
	# for username in itertools.product(string.letters, repeat=i):
for username in ['AAA', 'AABCDSSS'] * 3:
	r = requests.request('POST', "https://www.reddit.com/check_username", data=get_payload(''.join(username)),
						 headers=headers)
	if r.status_code == 429:
		print "Got 429"
	elif r.status_code == 200:
		print "Free user! {}".format(''.join(username))
	elif r.status_code == 400:
		print 'username: {} is already taken'.format(username)
	else:
		print "Got unexpected status {}".format(r.status_code)

