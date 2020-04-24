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

def country_dict(csv_data: List[Dict]) -> Dict:
    """
    calculate the average length of regions
    :param csv_data: A csv with the regions
    :return: Dictionary with the average length
    """
    countries = dict()
    sample = namedtuple("sample", "id length")
    for test in csv_data:
        id_sample, location, length = (test.get("Accession", " "),
                                       test.get("Geo_Location", " "),
                                       test.get("Length", ""))
        if location not in countries:
            countries[location] = [sample(id_sample, length)]
        else:
            countries[location].append(sample(id_sample, length))
    countries_ordered = {x: sorted(countries[x],
                                   key=lambda s: s.length)
                         for x in countries}
    target_samples = {c: countries_ordered[c][len(countries_ordered[c]) // 2]
                      for c in countries_ordered}
    return target_samples


def map_average(country_dict: dict) -> Dict:
    new_dict = dict()
    for country, value in country_dict.items():
        sorted_samples = sorted(value, key=lambda x: x[1])
        average = sorted_samples[len(sorted_samples) // 2]
        target_id = average[0]
        new_dict[country] = target_id
    return new_dict


def filter_country_average_length(data: List[Dict]) -> List[Dict]:
    country_dict = dict()
    for sample in data:
        rna_id, country, length = sample['Accession'], sample['Geo_Location'], sample['Length']
        country_dict.setdefault(country, []).append((rna_id, length))
    filtered_dict = map_average(country_dict)
    return list(filter(lambda sample: sample['Accession'] in filtered_dict.values(), data))

