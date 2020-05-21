"""
    Csv data processing module of the fasta data storage and reading implementation
"""
from csv import DictReader
from typing import List, Union, Dict

from prettytable import PrettyTable

import utils.select as sel


class CsvTable:
    """
    Helps to handle .csv files data and its processing
    :param: arg -> CSV filepath or information
    """

    def __init__(self, arg: Union[str, List[Dict]]):
        if isinstance(arg, str):
            self._table = self.__read(arg)
        elif isinstance(arg, list):
            self._table = arg
        else:
            raise TypeError("Invalid Argument")

    def __getitem__(self, index):
        try:
            return self._table[index]
        except IndexError:
            print("Index out of range")
            raise IndexError

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for row in self._table:
            yield row

    def __str__(self):
        pretty_table = PrettyTable(list(self._table[0].keys()))
        for row in self:
            pretty_table.add_row(row.values())
        return str(pretty_table)

    def values(self, column: str) -> List[str]:
        """
        :param column:
        :return List of values for this column:
        """
        try:
            return [row[column] for row in self]
        except:
            raise KeyError

    def dict_of(self, key, value):
        try:
            return dict(zip(self.values(key), self.values(value)))
        except:
            raise KeyError

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
        median_value = sel.quick_select_median(values, index=1)
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
            return list(map(dict, reader))
