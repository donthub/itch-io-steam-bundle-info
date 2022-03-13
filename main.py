import logging.config
import os

from excelprinter import ExcelPrinter
from itchiobundlegetter import ItchIoBundleGetter
from steamidnamegetter import SteamIdNameGetter
from steaminfofiller import SteamInfoFiller


def init_logging():
    os.makedirs('logs', exist_ok=True)
    logging.config.fileConfig('logging.conf')


def run():
    init_logging()
    logger = logging.getLogger(__name__)
    logger.info('Starting application')

    steam_id_name_getter = SteamIdNameGetter()
    bundle_info = ItchIoBundleGetter().get_bundle()
    SteamInfoFiller(steam_id_name_getter).fill_info(bundle_info)
    ExcelPrinter().print(bundle_info)

    logger.info('Exiting application')


if __name__ == '__main__':
    run()
