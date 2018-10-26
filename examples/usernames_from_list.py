#! /usr/bin/python3

# This module is an example for a simple usage of the reddit_session package
# This module demonstrates checking whether or not usernames are free from a list given in 'usernames_to_check.txt' file

from src.reddit_session import RedditSession


def main():
    rs = RedditSession()
    rs.initiate_session()

    with open('usernames_to_check.txt', 'r') as usernames:
        for username in usernames.readlines():
            username = username.strip()
            if rs.is_username_free(username):
                print('username {} is free!'.format(username))
            else:
                print('username {} is not free'.format(username))


if __name__ == '__main__':
    main()
