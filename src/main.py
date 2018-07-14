import itertools
import requests
import string
import time


headers = {
	'user-agent': 'my_crazy_bot',
	'cookie': 'rseor3=true; session=9045a3bc38f1c08687f937e64c31f9aa856a0751gAJKnjhKW0dB1tKMxifMNn1xAVUHX2NzcmZ0X3ECWCgAAAAyMzM0NTQ3NzJmMzIyZmQyMTNlZGQ5ZGM1YzBhMzFhMGE1MzgwNjY5cQNzh3EELg=='
}


def get_payload(username):
	return {'csrf_token': '233454772f322fd213edd9dc5c0a31a0a5380669', 'user': username}


def get_cookies():
	# TODO: implement this!
	pass


def get_csrf_token():
	# TODO: get csrf token
	pass


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

