import random
from collections import namedtuple
from csv import DictReader
from typing import List, Union, Dict

from prettytable import PrettyTable

from utils.select import quick_select_median


class CsvTable:
    """
    Helps to handle .csv files data and its processing
    :param: arg -> CSV filepath or information
    """

    def __init__(self, arg: Union[str, List[Dict]]):
        if isinstance(arg, str):
            self.__table = self.__read(arg)
        elif isinstance(arg, list):
            self.__table = arg
        else:
            raise TypeError("Invalid Argument")

    def __getitem__(self, index):
        try:
            return self.__table[index]
        except:
            raise IndexError("Index out of range")

    def __len__(self):
        return len(self.__table)

    def __iter__(self):
        for row in self.__table:
            yield row

    def __str__(self):
        pretty_table = PrettyTable(list(self.__table[0].keys()))
        for row in self:
            pretty_table.add_row(row.values())
        return str(pretty_table)

    def values(self, column):
        t = list()
        for row in self:
            t.append(row[column])
        return t

    def group_countries_by_median_length(self):
        """
        Filters the csv by country for average length's
        :return: CsvTable
        """
        country_dict = dict()
        for row, sample in enumerate(self):
            country = sample.get('Geo_Location', ' ').split(":")[0]
            length = sample['Length']
            country_dict.setdefault(country, []).append((row, length))
        filtered_data = [self.__get_average_row(country_dict[country])
                         for country in country_dict]
        return CsvTable(filtered_data)

    def __get_average_row(self, values: list) -> Union[dict, List[dict]]:
        median_value = quick_select_median(values, index=1)
        row = self[median_value[0]]
        geo_location = row['Geo_Location']
        row['Geo_Location'] = geo_location.split(":")[0] \
            if len(geo_location) > 0 \
            else "Unknown"
        return row

    @staticmethod
    def __read(file_path: str) -> List[Dict]:
        """
        Reads a csv file
        :return: List[Dict]
        """
        with open(file_path, 'r') as csv_file:
            reader = DictReader(csv_file, delimiter=',')
            return list(map(lambda row: dict(row), reader))
