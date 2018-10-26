#! /usr/bin/python3
# This module is an example for a possible usage of the 'reddit_session' package.
# This example uses itertools to create every possible combination of letters and numbers in order to find the shortest
# free username on reddit.com, starting from 3 letters.
# This usage was my original motivation for writing the package.

import itertools
import logging

from reddit_usernames.reddit_session import RedditSession


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    with open('free_usernames.txt', 'a') as free_usernames:
        find_shortest_username(free_usernames)


def find_shortest_username(output_file):
    '''
    This function finds the shortest free user names on reddit.com, and stores them in output_file
    '''
    rs = RedditSession()
    rs.initiate_session()

    count = 0
    for i in range(3, 6):
        for username in itertools.product('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456790_', repeat=i):
            count += 1
            username_string = ''.join(username)
            logging.debug('checking if username: {} is free'.format(username_string))
            if rs.is_username_free(username_string):
                logging.info('username {} is free!'.format(username_string))
                output_file.write(username_string + '\n')
                output_file.flush()
            if count % 100 == 0:
                logging.info('tried {} usernames'.format(count))


if __name__ == '__main__':
    main()
