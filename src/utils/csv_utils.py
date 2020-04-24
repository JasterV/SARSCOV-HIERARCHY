from csv import DictReader
from typing import List, Dict


def read_csv(file_path: str) -> List:
    """Reads a csv file and returns a list of Ordered Maps
    """
    with open(file_path, 'r') as csv_file:
        reader = DictReader(csv_file, delimiter=',')
        return list(reader)


# TODO: modify sorted, only if it is necessary.

def country_dict(csv_data: List[Dict]) -> Dict:
    """
    calculate the average length of regions
    :param csv_data: A csv with the regions
    :return: Dictionary with the average length
    """
    countries = dict()
    for test in csv_data:
        location = test.get("Geo_Location", " ")
        if location not in countries:
            numbers = filter(lambda x: x["Geo_Location"] == location, csv_data)
            countries[location] = sorted(
                list(x.get("Length") for x in numbers))
    return {c: countries[c][len(countries[c]) // 2] for c in countries}
