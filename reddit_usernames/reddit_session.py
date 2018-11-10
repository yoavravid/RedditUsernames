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
    SESSION_RE = re.compile('session=(?P<session>[a-zA-z0-9+]{150}==?);')

    def __init__(self):
        self._cookies = self.INITIAL_COOKIES
        self._headers = self.INITIAL_HEADERS
        self._headers['cookie'] = self._cookies_as_string
        self._initiate_session()

    def is_username_free(self, username):
        payload = {'csrf_token': self._csrf_token, 'user': username}
        response = requests.post(
            self.REDDIT_URL + '/check_username',
            headers=self.headers,
            data=payload
        )

        self._cookies['session'] = self._get_session_from_response(response)
        if response.status_code == 200:
            return True

        elif response.status_code == 400:
            return False

        else:
            raise RedditSessionError('Got unexpected return code {}'.format(response.status_code))

    @property
    def headers(self):
        # CR: Still don't like this property
        # CR: Why it is exported? why the users cares about the headers?
        # CR: A getter that changes _headers - looks bad
        self._headers['cookie'] = self._cookies_as_string
        return self._headers

    @property
    def _cookies_as_string(self):
        # CR: Its not really a property cookies_as_string, cookies is a property
        # CR: maybe static method cookie_to_string?
        """
        in this object we choose to manage the cookies as a dict, while in HTTP the cookies are managed as a string
        with a specific formatting. this function turns the dict into a cookie string in the HTTP form
        """

        return '; '.join('='.join(item) for item in self._cookies.items())

    def _initiate_session(self):
        """
        logic: 1st request to get the session tracker, 2nd request (to register) to get the csrf token and cookies
        then 'rolling' requests to check_username while updating the cookies every time
        """

        # CR: Use uniform style - change next line to use _initialize_session_tracker function
        self._cookies['session-tracker'] = self._get_session_tracker()
        register_request = requests.get(self.REDDIT_URL + '/register', headers=self.headers)
        self._initialize_cookies(register_request)
        # CR: Use uniform style - change next line to use _initialize_csrf_token function
        self._csrf_token = self._get_csrf_token(register_request)

    def _get_session_tracker(self):
        # CR: Can you get the session_tracker from the request in _initiate_session?
        response = requests.get(self.REDDIT_URL, headers=self.headers)
        return response.cookies['session_tracker']

    def _initialize_cookies(self, register_request):
        """ initializes the cookies according to the http response """

        self._cookies['session'] = self._get_session_from_response(register_request)
        # CR: session_tracker or session-tracker
        self._cookies.pop('session-tracker')

    @staticmethod
    def _get_session_from_response(response):
        match = RedditSession.SESSION_RE.search(response.headers['set-cookie'])
        return match.group('session')

    @staticmethod
    def _get_csrf_token(register_request):
        """ returns the csrf token """

        parsed_register_page = bs4.BeautifulSoup(register_request.content, 'html.parser')
        csrf_tokens = parsed_register_page.findAll("input", {"name": "csrf_token"})

        if len(csrf_tokens) != 1:
            raise RedditSessionError('Found invalid amount of csrf_tokens. Found {}, expecting {}'.format(len(csrf_tokens), 1))

        # CR: Validate the CSRF token value - does it have a fixed format?
        return csrf_tokens.pop()['value']
