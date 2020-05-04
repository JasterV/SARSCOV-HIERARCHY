from collections import namedtuple
from csv import DictReader
from typing import List, Union, Dict


from prettytable import PrettyTable


class CsvTable:
    """Helps to handle .csv files data and its processing
    Arguments: arg -> CSV filepath or information
    """

    def __init__(self, arg: Union[str, List[Dict]]):
        if isinstance(arg, str):
            self.__table = self.__read_csv(arg)
        elif isinstance(arg, list):
            self.__table = arg
        else:
            raise TypeError("Invalid Argument")

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__table[index]
        if abs(index) > len(self.__table):
            raise IndexError("Index out of range")
        return self.__table[index]

    def __len__(self):
        return len(self.__table)

    def __iter__(self):
        for row in self.__table:
            yield row

    def __str__(self):
        pretty_table = PrettyTable(['Accession', 'Release_Date', 'Species', 'Length',
                                    'Geo_Location', 'Host', 'Isolation_Source', 'Collection_Date'])
        for row in self:
            pretty_table.add_row(row.values())
        return str(pretty_table)

    def filter(self):
        """Filters the csv by country for average length's
        :return: CSV
        """
        country_dict = dict()
        named_sample = namedtuple("data_info", "row length")
        for row, sample in enumerate(self.__table):
            country, length = sample.get(
                'Geo_Location', 'Unknown'), sample['Length']
            country_dict.setdefault(country, []).append(
                named_sample(row, length))
        filtered_data = [self.__get_average_row(country_dict[country])
                         for country in country_dict]
        return CsvTable(filtered_data)

    @staticmethod
    def __read_csv(file_path: str) -> List[Dict]:
        """Reads a csv file
        :return: List[Dict]
        """
        with open(file_path, 'r') as csv_file:
            reader = DictReader(csv_file, delimiter=',')
            return list(map(lambda row: dict(row), reader))

    # TODO: modify sorted, only if it is necessary.

    def __get_average_row(self, values: tuple) -> Union[dict, List[dict]]:
        sorted_values = sorted(values, key=lambda x: x.length)
        average_value = sorted_values[len(values) // 2]
        return self.__table[average_value.row]
