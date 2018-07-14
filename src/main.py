import itertools
import requests
import string


headers = {
	'user-agent': 'my_crazy_bot',
	# Cookies hold lost of fields, by the form 'key'='value'; 'key'='value'. the order doesn't matter!
	'cookie': 'loid=00000000001rtgffkn.2.1531570301623.Z0FBQUFBQmJTZWg5NE1Hb0xyc0NDWTNxSHdyMG9kbWNqRl95UlE0Y3E5NkctMy1xUUFHWDVLNl83UF9qUHQtcTBUZ3lMdExwTmNWN3Y4RDNnaXIyZjdLWnR0MVhnMmVIYWpvTHRTc1Q2aEtZVnE2c1pnZFJtQTNnWUFSRkkwaElYNkNpWkFOSy1RenY; rseor3=true; rabt=; edgebucket=Q0a6zzbmhM4Z9k5UgJ; reddaid=2S56B2567L2OQCYA; USER=eyJwcmVmcyI6eyJwcm9maWxlTGF5b3V0IjoiTEFSR0UiLCJnbG9iYWxUaGVtZSI6IlJFRERJVCIsImVkaXRvck1vZGUiOiJyaWNodGV4dCIsImNvbW1lbnRNb2RlIjoicmljaHRleHQiLCJmZWF0dXJlc1ZpZXdlZEhpc3RvcnkiOnsiY29tbWVudEZvcm0iOnsibWFya2Rvd25Nb2RlTm90aWZpY2F0aW9uIjpmYWxzZX19LCJjb2xsYXBzZWRUcmF5U2VjdGlvbnMiOnsiZmF2b3JpdGVzIjpmYWxzZSwibXVsdGlzIjpmYWxzZSwibW9kZXJhdGluZyI6ZmFsc2UsInN1YnNjcmlwdGlvbnMiOmZhbHNlLCJwcm9maWxlcyI6ZmFsc2V9LCJuaWdodG1vZGUiOmZhbHNlLCJzdWJzY3JpcHRpb25zUGlubmVkIjpmYWxzZX0sImxhbmd1YWdlIjoiZW4ifQ==; session_tracker=nHjUYkTRZfEDTRpNcB.0.1531572808304.Z0FBQUFBQmJTZkpJYXM5MnIyaDFVR3BraHFrbmlvYUZZeHgzQ3M3OUFZUDNkQUtObmYteGhyX1BxdEhPUjI2YmdaSnB2UEkxZXVrXzQ3UEU3RkdKekFvd2JaRHdxSTNYcGpvU1dCZ1lGMG9nY1YxQ0g2X1FKS0N0MzU5dTFNS2hRRjBmYUM5Uk5PbUs; session=d6978b3d02c13336b2b8c390b743f7aa25b7da89gAJKhflJW0dB1tJ6Inq7mX1xAVUHX2NzcmZ0X3ECWCgAAAA3M2UxMjBiZGNiYjUzOTIyNjlkYTZhZmJhMDJmMzYxMzUzMzg0MTQ0cQNzh3EELg=='
}


def get_payload(username):
	return {'csrf_token': '73e120bdcbb5392269da6afba02f361353384144', 'user': username}


def get_cookies():
	# TODO: implement this!
	pass


def get_csrf_token():
	# TODO: get csrf token
	pass


counter = 0
valid_username_counter = 0
for i in xrange(3, 10):
	# for username in itertools.product(string.letters, repeat=i):
	for username in ['AABCDSSS', 'AAA']:
		if counter >= 0:
			r = requests.request('POST', "https://www.reddit.com/check_username", data=get_payload(''.join(username)),
								 headers=headers)
			if r.status_code == 429:
				print "Got 429"
			elif r.status_code == 200:
				print "Free user! {}".format(''.join(username))
				valid_username_counter += 1
			elif r.status_code == 400:
				print 'username: {} is already taken'.format(username)
				valid_username_counter = 0
			else:
				print "Got unexpected status {}".format(r.status_code)
		counter += 1

		if valid_username_counter > 4:
			raise IndexError('unlikely amount of consecutive valid unsernames. something probably went wrong!')

		if counter % 20 == 0:
			print 'tried {} usernames'.format(counter)

