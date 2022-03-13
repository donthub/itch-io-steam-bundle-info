import logging

import requests


class SteamIdNameGetter:
    FOLDER_NAME = 'cache'
    FILE_NAME = 'steamidnames.json'
    PATH_NAME = f'{FOLDER_NAME}/{FILE_NAME}'

    class SteamIdNotFoundException(Exception):
        pass

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.steam_id_names = self.init_steam_id_names()

    def init_steam_id_names(self) -> dict:
        self.logger.info('Retrieving Steam ID - name pairs')
        response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json')
        if response.status_code != 200:
            self.logger.error('Steam ID - name pairs could not be retrieved!')
            raise self.SteamIdNotFoundException()
        return response.json()

    def get_app_id(self, name) -> int:
        apps = self.steam_id_names['applist']['apps']
        for app in apps:
            if app['name'] == name:
                return app['appid']
        raise self.SteamIdNotFoundException()
