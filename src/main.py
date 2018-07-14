import itertools
import requests
import string



payload = {'csrf_token': 'f5da581ec015155c3723fec7a143f62d66880103', 'user': 'mmasdgfkjl'}
headers = {
    'User-agent': 'bot131',
    'origin': 'https://www.reddit.com',
    'referer': 'https://www.reddit.com/register?dest=https%3A%2F%2Fwww.reddit.com%2F',
    'Content-length': '66',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept-language': 'en-US,en;q=0.9,he;q=0.8',
    'Accept-encoding': 'gzip, deflate, br',
    'accept': '*/*',
    'cookie': 'loid=00000000001g748yjv.2.1527357045229.Z0FBQUFBQmJDWjUxeW95aFZIaVJramtBa2Z3RmlSdDRyLWFOSW83MlhrMGMwZ3NPNmNjOTlMbENQTGx6YXQzaUhOX1J1a0tfNnB1ejh4dG5ZUmRqNV9ZRFNRenFzT1M2WXUzLTFNTzJ6R1poR0NScV8yWXM5TDVRcDRhdVdaVmdTb2VUQ2ZmTmI0WXY; rabt=; edgebucket=Ka2No7MMBZh2nESyHW; _ga=GA1.2.1072815387.1527357065; _gid=GA1.2.42980862.1527357065; pc=eq; __utma=55650728.1072815387.1527357065.1527357067.1527357067.1; __utmc=55650728; __utmz=55650728.1527357067.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); reddaid=QCGIHL5W6DM46TAA; __gads=ID=074667ea30b77d59:T=1527357051:S=ALNI_MbJyzGMTAMWrQFGh7vQQiE4cmo88w; rseor3=true; uapp_cookie=3:1527210000; USER=eyJwcmVmcyI6eyJwcm9maWxlTGF5b3V0IjoiTEFSR0UiLCJnbG9iYWxUaGVtZSI6IlJFRERJVCIsImVkaXRvck1vZGUiOiJyaWNodGV4dCIsImNvbW1lbnRNb2RlIjoicmljaHRleHQiLCJmZWF0dXJlc1ZpZXdlZEhpc3RvcnkiOnsiY29tbWVudEZvcm0iOnsibWFya2Rvd25Nb2RlTm90aWZpY2F0aW9uIjpmYWxzZX19LCJjb2xsYXBzZWRUcmF5U2VjdGlvbnMiOnsiZmF2b3JpdGVzIjpmYWxzZSwibXVsdGlzIjpmYWxzZSwibW9kZXJhdGluZyI6ZmFsc2UsInN1YnNjcmlwdGlvbnMiOmZhbHNlLCJwcm9maWxlcyI6ZmFsc2V9fSwibGFuZ3VhZ2UiOiJlbiJ9; session=a06259bfa638c2e51849f0a838cd7c66c574661bgAJK9tEJW0dB1sJnqKEY0n1xAVUHX2NzcmZ0X3ECWCgAAAAyMzZhNDFhZThjZTFjZTQxZDU1MzUxODAzYTk2MjFlZWNkNjQ3YTgycQNzh3EELg=='
}


def get_payload(username):
    return {'csrf_token': '236a41ae8ce1ce41d55351803a9621eecd647a82', 'user': username}


# r = requests.request('POST', "https://www.reddit.com/check_username", data=get_payload('aaa'), headers=headers)
# print r.content

counter = 0
valid_username_counter = 0
for i in xrange(3, 10):
    for username in itertools.product(string.letters, repeat=i):
        if counter > 2460:
            r = requests.request('POST', "https://www.reddit.com/check_username", data=get_payload(''.join(username)),
                                 headers=headers)
            if r.status_code == 429:
                print "Got 429"
            elif r.status_code == 200:
                print "Free user! {}".format(''.join(username))
                valid_username_counter += 1
            elif r.status_code == 400:
                valid_username_counter = 0
            else:
                print "Got unexpected status"
        counter += 1

        if valid_username_counter > 4:
            raise IndexError('unlikely amount of consecutive valid unsernames. something probably went wrong!')

        if counter % 20 == 0:
            print 'tried {} usernames'.format(counter)

