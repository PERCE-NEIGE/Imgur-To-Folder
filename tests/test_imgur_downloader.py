from imgurtofolder.configuration import Configuration
from imgurtofolder.imgur_downloader import Imgur_Downloader
from os import makedirs
from os.path import expanduser, join, exists, dirname
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
