import itertools
import requests
import string
import time
import bs4

class RedditSession():
    '''
    a class used for managing a session with reddit.com
    note: it is mostly useful since it takes care of the cookies and the csrf token for you
    '''

    def __init__(self):
        # TODO: Should I seperate the init function and the actual initiation to another function?
        # for usage as follows:
        # s = RedditSession()
        # s.init()
        self._cookies = self._get_initial_cookies()
        self._csrf_token = self._get_csrf_token()

    def _get_initial_cookies(self):
        ''' returns the inital cookies '''
        pass

    def _get_csrf_token(self):
        ''' returns the csrf token '''
        pass
