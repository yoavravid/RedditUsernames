# Reddit usernames

This project's soul purpose is to find free usernames on [reddit](https://www.reddit.com/).

## Getting Started

The project is at its POC stage

1. Clone the repository
2. Open a session with 'reddit.com/register'
3. Enter a valid email
4. Open chrome's inspect -> network
5. Send a username
6. Replace the HTTP POST request's cookies and csrf token in main.py with the one's you find in the inspect
7. Run [main.py](main.py)

### Prerequisites

In order to run the program you will need to install [python 2.7](https://www.python.org/getit/)
(Add libraries)

## To Do List:
1. Implement the get_cookies function in main.py 
2. Implement the get_csrf function in main.py 

## Authors

* **Yoad Ravid** - *Initial work* - [yoavravid](https://github.com/yoavravid)
* **Steven Dashevsky** - *Changing readme* - [Steven17D](https://github.com/Steven17D)

See also the list of [contributors](https://github.com/yoavravid/reddit_usernames/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspired by this [reddit post](https://www.reddit.com/r/learnprogramming/comments/8m8hl3/python_script_to_look_for_free_username_on_a/)
