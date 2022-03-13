import os

import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from bundleinfo import BundleInfo


class ExcelPrinter:
    BUNDLE_ROW = 0
    HEADER_ROW = 1
    NAME_COL = 0
    SCORE_COL = 1
    POPULARITY_COL = 2
    PRICE_COL = 3
    URL_COL = 4

    def __init__(self):
        os.makedirs('output', exist_ok=True)

    def print(self, bundle_info: BundleInfo):
        workbook = xlsxwriter.Workbook(f'output/{bundle_info.bundle_id}.xlsx')
        worksheet = workbook.add_worksheet()
        self.print_header(workbook, worksheet, bundle_info)
        self.sort_games(bundle_info)
        self.print_rows(workbook, worksheet, bundle_info)
        self.filter_rows(worksheet, bundle_info)
        workbook.close()

    @staticmethod
    def print_header(workbook: Workbook, worksheet: Worksheet, bundle_info: BundleInfo):
        merge_format = workbook.add_format({'hyperlink': True, 'align': 'center'})
        worksheet.merge_range(ExcelPrinter.BUNDLE_ROW, ExcelPrinter.NAME_COL, ExcelPrinter.BUNDLE_ROW,
                              ExcelPrinter.URL_COL, f'https://itch.io/b/{bundle_info.bundle_id}/', merge_format)

        format_bold = workbook.add_format({'bold': 1})
        worksheet.write(ExcelPrinter.HEADER_ROW, ExcelPrinter.NAME_COL, 'Name', format_bold)
        worksheet.set_column(ExcelPrinter.NAME_COL, ExcelPrinter.NAME_COL, 45)
        worksheet.write(ExcelPrinter.HEADER_ROW, ExcelPrinter.SCORE_COL, 'Score', format_bold)
        worksheet.write(ExcelPrinter.HEADER_ROW, ExcelPrinter.POPULARITY_COL, 'Popularity', format_bold)
        worksheet.write(ExcelPrinter.HEADER_ROW, ExcelPrinter.PRICE_COL, 'Price', format_bold)
        worksheet.write(ExcelPrinter.HEADER_ROW, ExcelPrinter.URL_COL, 'URL', format_bold)
        worksheet.set_column(ExcelPrinter.URL_COL, ExcelPrinter.URL_COL, 42)

        worksheet.autofilter(ExcelPrinter.HEADER_ROW, ExcelPrinter.NAME_COL, ExcelPrinter.HEADER_ROW,
                             ExcelPrinter.URL_COL)

    @staticmethod
    def print_rows(workbook: Workbook, worksheet: Worksheet, bundle_info: BundleInfo):
        format_percentage = workbook.add_format({'num_format': '0.00%'})
        row = ExcelPrinter.HEADER_ROW + 1
        for game in bundle_info.games:
            worksheet.write(row, ExcelPrinter.NAME_COL, game.name)
            if game.total_reviews:
                worksheet.write(row, ExcelPrinter.SCORE_COL, game.total_positive / game.total_reviews,
                                format_percentage)
                worksheet.write(row, ExcelPrinter.POPULARITY_COL, game.total_reviews)
            worksheet.write(row, ExcelPrinter.PRICE_COL, game.price)
            if game.app_id:
                worksheet.write(row, ExcelPrinter.URL_COL, f'https://store.steampowered.com/app/{game.app_id}/')
            row += 1

    @staticmethod
    def filter_rows(worksheet: Worksheet, bundle_info: BundleInfo):
        worksheet.filter_column(ExcelPrinter.URL_COL, 'x == NonBlanks')

        row = ExcelPrinter.HEADER_ROW + 1
        for game in bundle_info.games:
            if game.app_id:
                pass
            else:
                worksheet.set_row(row, options={'hidden': True})
            row += 1

    @staticmethod
    def sort_games(bundle_info: BundleInfo):
        bundle_info.games.sort(key=lambda x: x.total_reviews if x.total_reviews else 0, reverse=True)
