from collections import namedtuple
from csv import DictReader
from typing import List, Dict


def read_csv(file_path: str) -> List:
    """Reads a csv file and returns a list of Ordered Maps
    """
    with open(file_path, 'r') as csv_file:
        reader = DictReader(csv_file, delimiter=',')
        return list(reader)


# TODO: modify sorted, only if it is necessary.

def get_average_row(csv_data: List[Dict], values: tuple) -> int:
    sorted_values = sorted(values, key=lambda x: x.length)
    average_value = sorted_values[len(values) // 2]
    return csv_data[average_value.row]


def filter_country_average_length(data: List[Dict]) -> List[int]:
    """
    calculate the average length of regions
    :param data: A csv with the regions
    :return: list csv with the average length on region
    """
    country_dict = dict()
    named_sample = namedtuple("data_info", "row length")
    for row, sample in enumerate(data):
        country, length = sample.get(
            'Geo_Location', 'Unknown'), sample['Length']
        country_dict.setdefault(country, []).append(named_sample(row, length))
    return [get_average_row(data, country_dict[country])
            for country in country_dict]
