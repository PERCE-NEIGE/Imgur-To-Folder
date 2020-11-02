from imgurtofolder.configuration import Configuration
from imgurtofolder.imgur_downloader import Imgur_Downloader
from os import makedirs, listdir, remove, rmdir
from os.path import expanduser, join, exists, dirname, isfile
import json
import pytest

CONFIG_PATH = join(expanduser('~'), ".config", "imgurToFolder", 'config.json')


@pytest.fixture
def imgur_downloader():
    """Pytest fixture to yield an Imgur object"""
    if not exists(CONFIG_PATH):
        makedirs(dirname(CONFIG_PATH), exist_ok=True)

        with open(CONFIG_PATH, 'w') as current_file:
            current_file.write(json.dumps(dict(
                access_token="",
                client_id="",
                client_secret="",
                download_path="",
                refresh_token="")))

    with open(CONFIG_PATH, 'r') as current_file:
        data = json.loads(current_file.read())

        configuration = Configuration(
            config_path=CONFIG_PATH,
            access_token=data['access_token'],
            client_id=data['client_id'],
            client_secret=data['client_secret'],
            download_path=data['download_path'],
            refresh_token=data['refresh_token'],
            overwrite=False
        )

    imgur_downloader = Imgur_Downloader(configuration,
                                        max_favorites=80)

    yield imgur_downloader


def test_replace_characters(imgur_downloader):
    invalid_word = "\\a'b/c:d*e?f\"g<h>i|j.k\nl"
    valid_word = imgur_downloader.replace_characters(invalid_word)
    assert valid_word == 'abcdefghijkl'


def test_parse_id(imgur_downloader):
    # Get album id
    found_id = imgur_downloader.parse_id('https://imgur.com/a/aAlbumTag')
    assert found_id == ('album', 'aAlbumTag')

    # Get Gallery id
    found_id = imgur_downloader.parse_id('https://imgur.com/g/aGalleryTag')
    assert found_id == ('gallery', 'aGalleryTag')

    # Get Gallery id
    found_id = imgur_downloader.parse_id('https://imgur.com/gallery/1QJQv4B')
    assert found_id == ('gallery', '1QJQv4B')

    # Get Subreddit id
    found_id = imgur_downloader.parse_id('https://imgur.com/r/funny')
    assert found_id == ('subreddit', 'funny')

    # Get Subreddit id photo
    found_id = imgur_downloader.parse_id('https://imgur.com/r/funny/TZI385c')
    assert found_id == ('subreddit', 'funny/TZI385c')

    # Get tag
    found_id = imgur_downloader.parse_id('https://imgur.com/t/someTag')
    assert found_id == ('tag', 'someTag')


def test_download_album(imgur_downloader): 
    # Get Album id 
    test_album = 'https://imgur.com/a/0u4eQ'
    test_album_type, test_album_id = imgur_downloader.parse_id(test_album)
    assert test_album_type == 'album'
    
    # Test Album Download
    imgur_downloader.download_album(test_album_id)
    path = join(imgur_downloader._configuration.get_download_path(), 'wallpapers')
    count = len([name for name in listdir(path) if isfile(join(path, name))])
    assert count == 100

    # Deleting created images
    for name in listdir(path): 
        full_file_path = join(path, name)
        if isfile(full_file_path):
            remove(full_file_path)
            assert not exists(full_file_path)

    # Deleting empty download directory
    rmdir(path)
    assert not exists(path)