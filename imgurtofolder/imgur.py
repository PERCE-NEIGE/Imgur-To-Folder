from .logs import Log
from pprint import pformat
from time import sleep
import os
import re
import requests
import webbrowser


class Imgur:

    _log = Log('imgur')

    def __init__(self, configuration):
        self._log.debug('Configuration set')
        self._configuration = configuration

    def set_configuration(self, configuration):
        self._log.debug('Changed configuration')
        self._configuration = configuration

    def set_download_path(self, path):
        self._log.debug('Changing download path')
        if not os.path.exists(path):
            os.makedirs(path)
        self._configuration.set_download_path(path)

    def set_default_folder_path(self, path):
        self._log.debug('Changing download path')
        if not os.path.exists(path):
            os.makedirs(path)
        self._configuration.set_default_download_path(path)

    def get_download_path(self):
        return self._configuration.get_download_path()

    def get_overwrite(self):
        return self._configuration.get_overwrite()

    def authorize(self):
        url = "https://api.imgur.com/oauth2/authorize?response_type=token&client_id={client_id}".format(
            client_id=self._configuration.get_client_id()
        )

        # Have user authorize their own app
        webbrowser.open_new(url)
        self._log.info("If a webpage did not load please go to: %s" % url)
        self._log.info(
            "This gives ImgurToFolder permission to view account information.")
        self._log.info(
            "ImgurToFolder does NOT collect any passwords or personal info!")

        # Have user paste their own repsonse url
        self._log.info("---")
        self._log.info("After you loged in, you'll see the Imgur homepage.")
        user_input = str(input("Paste the redirected url here: "))

        # Save access_token and refresh_token to users config
        access_token = re.search(r'access_token=(\w+)', user_input).group(1)
        refresh_token = re.search(r'refresh_token=(\w+)', user_input).group(1)
        self._configuration.set_access_token(access_token)
        self._configuration.set_refresh_token(refresh_token)
        self._configuration.save_configuration()
        self._log.debug('Configuration saved')
        self._log.info('The application is now authorized')

    def generate_access_token(self):
        url = 'https://api.imgur.com/oauth2/token'
        data = {'refresh_token': self._configuration.get_refresh_token(),
                'client_id': self._configuration.get_client_id(),
                'client_secret': self._configuration.get_client_secret(),
                'grant_type': 'refresh_token'}
        headers = {
            'Authorization': 'Bearer %s' % self._configuration.get_access_token()
        }
        response = requests.request('POST',
                                    url,
                                    headers=headers,
                                    data=data,
                                    allow_redirects=False)
        response_json = response.json()

        self._configuration.set_access_token(response_json['access_token'])

    def get_account_images(self, username, page=0):
        pass

    def get_gallery_favorites(self, username, sort='newest'):
        pass

    def get_account_favorites(self, username, sort='newest', page=0, max_items=-1):
        pass

    def get_account_submissions(self, username):
        url = f'https://api.imgur.com/3/account/{username}/submissions/'
        headers = {
            'Authorization': 'Client-ID %s' % self._configuration.get_client_id()
        }
        response = requests.request('GET', url, headers=headers)
        return response.json()

    def get_album(self, album_hash):
        url = f'https://api.imgur.com/3/album/{album_hash}'
        headers = {
            'Authorization': 'Client-ID %s' % self._configuration.get_client_id()
        }
        response = requests.request('GET', url, headers=headers)
        return response.json()

    def get_gallery_album(self, gallery_hash):
        url = f'https://api.imgur.com/3/gallery/{gallery_hash}'
        headers = {
            'Authorization': 'Client-ID %s' % self._configuration.get_client_id()
        }
        response = requests.request('GET', url, headers=headers)
        return response.json()

    def get_subreddit_gallery(self, subreddit, sort='time', window='day', page=0):
        url = f'https://api.imgur.com/3/gallery/r/{subreddit}/{sort}/{window}/{page}'
        headers = {
            'Authorization': 'Client-ID %s' % self._configuration.get_client_id()
        }
        response = requests.request('GET', url, headers=headers)
        return response.json()

    def get_subreddit_image(self, subreddit, image_id):
        url = f'https://api.imgur.com/3/gallery/r/{subreddit}/{image_id}'
        headers = {
            'Authorization': 'Client-ID %s' % self._configuration.get_client_id()
        }
        response = requests.request('GET', url, headers=headers)
        return response.json()

    def get_tag(self, tag, sort='top', window='week', page=0, max_items=30):
        pass 