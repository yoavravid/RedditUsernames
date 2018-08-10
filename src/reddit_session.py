import itertools
import requests
import string
import time
# import bs4

class RedditSession():
    '''
    a class used for managing a session with reddit.com
    note: it is mostly useful since it takes care of the cookies and the csrf token for you
    '''

    INITIAL_COOKIES = {'rseor3': 'true'}
    INITIAL_HEADERS = {'user-agent': 'my_crazy_bot'}

    def __init__(self):
        self._cookies = self.INITIAL_COOKIES
        self._headers = self.INITIAL_HEADERS
        self._headers['cookies'] = self._cookies_as_string


    def init(self):
        # logic: 1st request to get the session tracker, 2nd request (to register) to get the csrf token and cookies
        # then 'rolling' requests to check_username while updating the cookies everytime
        self._cookies['session-tracker'] = self._get_session_tracker()
        self._register_request =
        self._cookies = self._get_initial_cookies()
        self._csrf_token = self._get_csrf_token()

    @property
    def _cookies_as_string(self):
        return '; '.join('='.join(item) for item in self._cookies.items())

    def _get_session_tracker(self):
        pass


    def _get_initial_cookies(self):
        ''' returns the inital cookies '''
        pass

    def _get_csrf_token(self):
        ''' returns the csrf token '''
        # play with ipython until you find an easy way to get the cookies from the request
        pass
