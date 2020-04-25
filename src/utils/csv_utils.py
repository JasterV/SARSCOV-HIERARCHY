from collections import namedtuple
from csv import DictReader
from typing import List, Union


class CSV:
    def __init__(self, path_file=None, table=None):
        if path_file is not None:
            self.__csv_list = self.__read_csv(path_file)
        elif table is not None:
            self.__csv_list = table
        else:
            raise TypeError("Invalid arguments")

    @staticmethod
    def __read_csv(file_path: str) -> List:
        """Reads a csv file and returns a list of Ordered Maps
        """
        with open(file_path, 'r') as csv_file:
            reader = DictReader(csv_file, delimiter=',')
            return list(reader)

    # TODO: modify sorted, only if it is necessary.

    def __get_average_row(self, values: tuple) -> Union[dict, List[dict]]:
        sorted_values = sorted(values, key=lambda x: x.length)
        average_value = sorted_values[len(values) // 2]
        return self.__csv_list[average_value.row]

    def filter(self):
        """
        calculate the average length of regions
        :return: csv instance with the average length on region
        """
        country_dict = dict()
        named_sample = namedtuple("data_info", "row length")
        for row, sample in enumerate(self.__csv_list):
            country, length = sample.get(
                'Geo_Location', 'Unknown'), sample['Length']
            country_dict.setdefault(country, []).append(named_sample(row, length))
        filtered_data = [self.__get_average_row(country_dict[country])
                         for country in country_dict]
        return CSV(table=filtered_data)
