import logging
import re

import requests as requests
from easygui import enterbox

from bundleinfo import BundleInfo


class ItchIoBundleGetter:
    class InvalidItchIoBundleException(Exception):
        pass

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_bundle(self) -> BundleInfo:
        url_or_id = enterbox('Please enter Itch.io bundle URL or ID:')
        pattern = re.compile(r'^https://itch\.io/b/(\d+)/(.*)$|^(\d+)$')
        match = pattern.match(url_or_id)
        if not match:
            self.logger.error('Provided Itch.io bundle URL or ID is invalid!')
            raise self.InvalidItchIoBundleException()
        id = match.group()

        self.logger.info('Retrieving bundle information from Itch.io')
        response = requests.get(f'https://itch.io/bundle/{id}/games.json')
        if response.status_code != 200:
            self.logger.error('Could not retrieve Itch.io bundle information!')
            raise self.InvalidItchIoBundleException()

        json = response.json()
        return self.convert(id, json)

    @staticmethod
    def convert(id, json) -> BundleInfo:
        games = json['games']
        bundle_info = BundleInfo()
        bundle_info.bundle_id = id
        for game in games:
            game_info = BundleInfo.GameInfo()
            game_info.name = game['title']
            bundle_info.games.append(game_info)
        return bundle_info
