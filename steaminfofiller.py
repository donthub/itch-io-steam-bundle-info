import logging

import requests

from bundleinfo import BundleInfo
from steamidnamegetter import SteamIdNameGetter


class SteamInfoFiller:
    class SteamInfoNotFoundException(Exception):
        pass

    def __init__(self, steam_id_name_getter: SteamIdNameGetter):
        self.logger = logging.getLogger(__name__)
        self.steam_id_name_getter = steam_id_name_getter

    def fill_info(self, itch_io_bundle: BundleInfo):
        self.logger.info('Retrieving games information from Steam')
        counter = 1
        size = len(itch_io_bundle.games)
        for game in itch_io_bundle.games:
            self.logger.debug(f'Retrieving game information from Steam ({counter}/{size}) - {game.name}')
            try:
                game.app_id = self.steam_id_name_getter.get_app_id(game.name)
                self.fill_review_info(game)
                self.fill_other_info(game)
            except (SteamIdNameGetter.SteamIdNotFoundException, self.SteamInfoNotFoundException):
                pass
            counter += 1

    def fill_review_info(self, game: BundleInfo.GameInfo):
        response = requests.get(f'https://store.steampowered.com/appreviews/{game.app_id}?json=1')
        if response.status_code != 200:
            raise self.SteamInfoNotFoundException()

        query_summary = response.json()['query_summary']
        game.total_reviews = query_summary['total_reviews']
        game.total_positive = query_summary['total_positive']

    def fill_other_info(self, game: BundleInfo.GameInfo):
        response = requests.get(f'https://store.steampowered.com/api/appdetails?appids={game.app_id}')
        if response.status_code != 200:
            raise self.SteamInfoNotFoundException()

        data = response.json()[str(game.app_id)]['data']
        if 'price_overview' in data:
            game.price = data['price_overview']['initial'] / 100
