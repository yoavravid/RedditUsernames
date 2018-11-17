import requests
import bs4
import re


class RedditSessionError(Exception):
    pass


class RedditSession:
    """
    a class used for managing a session with reddit.com
    note: it is mostly useful since it takes care of the cookies and the csrf token for you
    note: the cookies are handled as a dict and the 'cookie_as_string' re-formats them to a cookie-string format.
    """

    REDDIT_URL = 'https://www.reddit.com'
    INITIAL_COOKIES = {'rseor3': 'true'}
    INITIAL_HEADERS = {'user-agent': 'my_crazy_bot'}
    SESSION_PATTERN = re.compile('session=(?P<session>[a-zA-z0-9+]{150}==?);')
    CSRF_TOKEN_PATTERN = re.compile('(?P<csrf_token>[a-f0-9]{40}?)')

    def __init__(self):
        self._cookies = self.INITIAL_COOKIES
        self._headers = self.INITIAL_HEADERS
        self._headers['cookie'] = self._cookies_as_string(self._cookies)
        self._initiate_session()

    def is_username_free(self, username):
        payload = {'csrf_token': self._csrf_token, 'user': username}
        response = requests.post(
            self.REDDIT_URL + '/check_username',
            headers=self._get_formatted_headers(),
            data=payload
        )

        self._cookies['session'] = self._get_session_from_response(response)
        if response.status_code == 200:
            return True

        elif response.status_code == 400:
            return False

        else:
            raise RedditSessionError('Got unexpected return code {}'.format(response.status_code))

    def _get_formatted_headers(self):
        self._headers['cookie'] = self._cookies_as_string(self._cookies)
        return self._headers

    @staticmethod
    def _cookies_as_string(cookies):
        """
        In this object we choose to manage the cookies as a dict, while in HTTP the cookies are managed as a string
        with a specific formatting. this function turns the dict into a cookie string in the HTTP form
        """

        return '; '.join('='.join(item) for item in cookies.items())

    def _initiate_session(self):
        """
        1st request to get the session tracker, 2nd request (to register) to get the csrf token and cookies
        then 'rolling' requests to check_username while updating the cookies every time
        """

        register_request = requests.get(self.REDDIT_URL + '/register', headers=self._get_formatted_headers())
        self._cookies['session'] = self._get_session_from_response(register_request)
        self._csrf_token = self._get_csrf_token_from_response(register_request)

    @staticmethod
    def _get_session_from_response(response):
        match = RedditSession.SESSION_PATTERN.search(response.headers['set-cookie'])
        return match.group('session')

    @staticmethod
    def _get_csrf_token_from_response(register_request):
        """ returns the csrf token """

        parsed_register_page = bs4.BeautifulSoup(register_request.content, 'html.parser')
        csrf_tokens = parsed_register_page.findAll("input", {"name": "csrf_token"})

        if len(csrf_tokens) != 1:
            raise RedditSessionError('Found invalid amount of csrf_tokens. Found {}, expecting {}'.format(len(csrf_tokens), 1))

        csrf_token = csrf_tokens.pop()['value']
        if not RedditSession.CSRF_TOKEN_PATTERN.match(csrf_token):
            raise RedditSessionError(f'Got invalid csrf_token from server: {csrf_token}')
        return csrf_token
