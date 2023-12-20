from setuptools import setup

setup(
   name='gachaBot',
   version='1.0',
   description='A useful module',
   author='Alex',
   author_email='maxhale4@gmail.com',
   packages=['gachaBot'],  #same as name
   install_requires=['youtube_dl', 'discord', 'python-dotenv', 'youtube_search', 'yt_dlp'], #external packages as dependencies
)