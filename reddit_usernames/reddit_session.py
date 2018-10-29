import requests
import bs4
import re


class RedditSession:
    """
    a class used for managing a session with reddit.com
    note: it is mostly useful since it takes care of the cookies and the csrf token for you
    note: the cookies are handled as a dict and the 'cookie_as_string' re-formats them to a cookie-string format.
    """

    REDDIT_URL = 'https://www.reddit.com'
    INITIAL_COOKIES = {'rseor3': 'true'}
    INITIAL_HEADERS = {'user-agent': 'my_crazy_bot'}

    def __init__(self):
        self._cookies = self.INITIAL_COOKIES
        self._headers = self.INITIAL_HEADERS
        self._headers['cookie'] = self._cookies_as_string
        self._csrf_token = ''
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
            # CR: RedditSessionError?
            raise ValueError('Got unexpected return code {}'.format(response.status_code))

    @property
    def headers(self):
        # CR: Look odd - why a getter modifies the header?
        self._headers['cookie'] = self._cookies_as_string
        return self._headers

    @property
    def _cookies_as_string(self):
        """
        in this object we choose to manage the cookies as a dict, while in HTTP the cookies are managed as a string
        with a specific formatting. this function turns the dict into a cookie string in the HTTP form
        """

        return '; '.join('='.join(item) for item in self._cookies.items())

    def _initiate_session(self):
        # logic: 1st request to get the session tracker, 2nd request (to register) to get the csrf token and cookies
        # then 'rolling' requests to check_username while updating the cookies every time

        self._cookies['session-tracker'] = self._get_session_tracker()
        register_request = requests.get(self.REDDIT_URL + '/register', headers=self.headers)
        self._initialize_cookies(register_request)
        self._csrf_token = self._get_csrf_token(register_request)

    def _get_session_tracker(self):
        response = requests.get(self.REDDIT_URL, headers=self.headers)
        return response.cookies['session_tracker']

    def _initialize_cookies(self, register_request):
        """ initializes the cookies according to the http response """

        self._cookies['session'] = self._get_session_from_response(register_request)
        self._cookies.pop('session-tracker')

    @staticmethod
    def _get_session_from_response(response):
        # CR: Compile the regex only once
        # CR: Don't use .* be more specific - session string has a fixed set of characters
        match = re.search('session=(?P<session>.*?);', response.headers['set-cookie'])
        return match.group('session')

    @staticmethod
    def _get_csrf_token(register_request):
        """ returns the csrf token """

        # CR: Meaningful naming?
        bs = bs4.BeautifulSoup(register_request.content, 'html.parser')
        # CR: Can you use bs to find by name?
        csrf_tokens = set(html_input for html_input in bs.find_all('input') if html_input['name'] == 'csrf_token')

        if len(csrf_tokens) != 1:
            # CR: RedditSessionError
            raise ValueError('Found invalid amount of csrf_tokens. Found {}, expecting {}'.format(len(csrf_tokens), 1))

        # CR: Don't you want to convert it to string from unicode before return?
        return csrf_tokens.pop()['value']

