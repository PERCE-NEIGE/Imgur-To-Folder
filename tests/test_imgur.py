from imgurtofolder.configuration import Configuration
from imgurtofolder.imgur import Imgur
from os import listdir
from os.path import expanduser, exists, join, isfile
import json
import pytest

CONFIG_PATH = join(expanduser('~'), ".config", "imgurToFolder", 'config.json')


@pytest.fixture
def imgur():
    """Pytest fixture to yield an Imgur object"""
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

    imgur = Imgur(configuration)

    yield imgur


def test_set_download_path(imgur):
    """Testing if set_download_path sets the download path to an Imgur Object"""
    old_path = join(expanduser('~'), "Downloads")
    new_path = join(expanduser('~'), "Downloads", "testFolderItf")

    imgur.set_download_path(new_path)
    assert imgur.get_download_path() == join(expanduser('~'),
                                             "Downloads",
                                             "testFolderItf")
    assert imgur._configuration.get_download_path() == join(expanduser('~'),
                                                            "Downloads",
                                                            "testFolderItf")

    imgur.set_download_path(old_path)
    assert imgur.get_download_path() == old_path
    assert imgur._configuration.get_download_path() == old_path


def test_set_default_folder_path(imgur):
    """Testing if set_default_download_path sets the download path to an Imgur Object and config file"""
    old_path = join(expanduser('~'), "Downloads")
    new_path = join(expanduser('~'), "Downloads", "testFolderItf")

    imgur.set_default_folder_path(new_path)
    assert imgur.get_download_path() == join(expanduser('~'),
                                             "Downloads",
                                             "testFolderItf")
    assert imgur._configuration.get_download_path() == join(expanduser('~'),
                                                            "Downloads",
                                                            "testFolderItf")
    with open(CONFIG_PATH, 'r') as current_file:
        data = json.loads(current_file.read())
        assert data['download_path'] == imgur.get_download_path()

    imgur.set_default_folder_path(old_path)
    assert imgur.get_download_path() == old_path
    assert imgur._configuration.get_download_path() == old_path

    with open(CONFIG_PATH, 'r') as current_file:
        data = json.loads(current_file.read())
        assert data['download_path'] == old_path


def test_get_download_path(imgur):
    """Testing if get_download_path gets the correct configuration download path from an Imgur Object"""

    download_path = imgur.get_download_path()

    with open(CONFIG_PATH, 'r') as current_file:
        data = json.loads(current_file.read())
        assert download_path == data['download_path']


def test_get_overwrite(imgur):
    """Testing if overwrite field is returned from config file"""

    overwrite = imgur.get_overwrite()

    with open(CONFIG_PATH, 'r') as current_file:
        data = json.loads(current_file.read())
        assert overwrite == data['overwrite']


@pytest.mark.skip("Skipping to not pause tests... Should work.")
def test_authorize(imgur):

    imgur.authorize()

    assert imgur._configuration.get_access_token()
    assert imgur._configuration.get_refresh_token()

    with open(CONFIG_PATH, 'r') as current_file:
        data = json.loads(current_file.read())
        assert data['access_token']
        assert data['refresh_token']


def test_get_account_images(imgur):
    """Test retrival of account images."""
    account_images = imgur.get_account_images("me", starting_page=0)
    assert len(account_images) > 1


def test_get_gallery_favorites(imgur):
    account_gallery_favorites = imgur.get_gallery_favorites("me",
                                                            sort="newest")
    assert len(account_gallery_favorites) > 1

    account_gallery_favorites = imgur.get_gallery_favorites("me",
                                                            sort="oldest")
    assert len(account_gallery_favorites) > 1


def test_get_account_favorites(imgur):
    account_gallery_favorites = imgur.get_account_favorites("me",
                                                            sort="newest")
    assert len(account_gallery_favorites) > 1

    account_gallery_favorites = imgur.get_account_favorites("me",
                                                            sort="oldest")
    assert len(account_gallery_favorites) > 1


def test_get_tag(imgur):
    

    total_images = imgur.get_tag('programming',
                                 sort='top',
                                 window='all',
                                 starting_page=0,
                                 max_items=10)

    assert len(total_images) == 10

    total_images = imgur.get_tag('programming',
                                 sort='time',
                                 window='day',
                                 starting_page=0,
                                 max_items=11)

    assert len(total_images) == 11

    total_images = imgur.get_tag('programming',
                                 sort='time',
                                 window='week',
                                 starting_page=0,
                                 max_items=12)

    assert len(total_images) == 12

    total_images = imgur.get_tag('programming',
                                 sort='time',
                                 window='month',
                                 starting_page=0,
                                 max_items=13)

    assert len(total_images) == 13

    total_images = imgur.get_tag('programming',
                                 sort='time',
                                 window='year',
                                 starting_page=0,
                                 max_items=15)

    assert len(total_images) == 15
