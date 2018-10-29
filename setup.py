from setuptools import setup

setup(name='reddit_usernames',
      version='0.1',
      description='Library for finding free usernames on reddit',
      url='http://github.com/yoavravid/RedditUsernames',
      author='Yoav Ravid',
      author_email='yravid@gmail.com',
      license='MIT',
      packages=['reddit_usernames'],
      install_requires=[
          'bs4',
          'requests',
      ],
      zip_safe=False)
