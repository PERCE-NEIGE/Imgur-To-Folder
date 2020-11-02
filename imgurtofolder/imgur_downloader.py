# Derek Santos
from .imgur import Imgur
from .logs import Log
from time import sleep
import os
import re
import requests
import shutil


class Imgur_Downloader(Imgur):

    _log = Log('downloader')

    def __init__(self, configuration, max_favorites):
        super().__init__(configuration)
        self._max_favorites = max_favorites

    def replace_characters(self, word):
        """Replace filesystem invalid characters"""
        invalid_characters = ['\\', "'", '/', ':',
                              '*', '?', '"', '<',
                              '>', '|', '.', '\n']
        for character in invalid_characters:
            word = word.replace(character, '')
        word = word.strip()
        return word

    def parse_id(self, url):
        """Pare a single url and return (imgurtype, imgurid)"""
        imgur_base_extensions = {
            'album': [r'(/a/)(\w+)'],
            'gallery': [r'(/g/)(\w+)', r'(/gallery/)(\w+)'],
            'subreddit': [r'(/r/)(\w+\/\w+)', r'(/r/)(\w+)$'],
            'tag': [r'(/t/)(\w+)']
        }

        # Parsing Album
        for imgur_type in imgur_base_extensions.keys():
            for extension in imgur_base_extensions[imgur_type]:
                value = re.search(extension, url)
                if value is not None:
                    return (imgur_type, value.group(2))

        # If still not found raise exception
        raise UrlIdNotFoundError('ID structure not found')

    def get_image_link(self, image):
        if 'mp4' in image:
            return image['mp4']
        elif 'gifv' in image:
            return image['gifv']
        else:
            return image['link']

    def download_tag(self, id, page=0, max_items=30):
        """Recieves a tag id, retieves metadata about tag, then proceeds to download tag images."""
        # TODO: Tag Download
        pass

    def download_album(self, id):
        """Recieves an album id, retieves metadata about album, then proceeds to download album images."""

        self._log.debug('Getting album details')
        album = self.get_album(id)
        title = album['title'] if album['title'] else album['id']
        title = self.replace_characters(title)
        path = os.path.join(self._configuration.get_download_path(), title)

        self._log.debug("Checking if folder exists")
        if not os.path.exists(path):
            self._log.debug("Creating folder: %s" % path)
            os.makedirs(path)

        self._log.info('Downloading album: %s' % title)
        for position, image in enumerate(album['images'], start=1):
            image_link = self.get_image_link(image)
            image_filename = "{} - {}{}".format(album['id'],
                                                position,
                                                image_link[image_link.rfind('.'):])

            self.download(image_filename, image_link, path)

    def download_gallery(self, id):
        # TODO: Download Gallery
        pass

    def download_subreddit(self, subreddit, sort='time', window='day', page=0, max_items=30):
        # TODO: Subreddit Download
        pass

    def download_subreddit_gallery(self, subreddit, id):
        # TODO: Subreddit gallery ?
        pass

    def download_favorites(self, username, latest=True, page=0, max_items=None):
        # TODO: Download favorites
        pass

    def download_account_images(self, username, page=0, max_items=None):
        # TODO: Download account images
        pass

    def download(self, filename, url, path):

        self._log.debug('Checking that folder path exists')
        if not os.path.exists(path):
            self._log.debug('Creating folder path')
            os.makedirs(path)

        self._log.debug('Checking to overwrite')
        if not self._configuration.get_overwrite() and os.path.exists(os.path.join(path, filename)):
            self._log.info('\tSkipping %s' % filename)
            return

        req = requests.get(url, stream=True)
        if req.status_code == 200:
            file_size = int(req.headers.get(
                'content-length', 0)) / float(1 << 20)
            self._log.info('\t%s, File Size: %.2f MB' % (filename, file_size))
            with open(os.path.join(path, filename), 'wb') as image_file:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, image_file)
        else:
            self._log.info('\tERROR! Can not download: ' +
                           os.path.join(path, filename))
            self._log.info('\tStatus code: ' + str(req.status_code))

        # Delaying so no timeout
        sleep(.1)


class UrlIdNotFoundError(Exception):
    pass
