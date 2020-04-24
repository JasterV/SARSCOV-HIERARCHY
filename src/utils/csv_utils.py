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
    countries_ordered = {
        x: sorted(countries[x], key=lambda s: s.length) for x in countries}
    target_samples = {c: countries_ordered[c][len(
        countries_ordered[c]) // 2] for c in countries_ordered}
    return target_samples


def get_average_id(values):
    sorted_values = sorted(values, key=lambda x: x[1])
    average_value = sorted_values[len(values) // 2]
    sample_id = average_value[0]
    return sample_id

def filter_country_average_length(data: List[Dict]) -> List[Dict]:
    country_dict = dict()
    for sample in data:
        # Creem les llistes de tuples id-length
        rna_id, country, length = sample['Accession'], sample['Geo_Location'], sample['Length']
        country_dict.setdefault(country, []).append((rna_id, length))
    # Transformem el diccionari a un diccionari country - average_id
    new_dict = {country: get_average_id(country_dict[country]) 
                              for country in country_dict}
    # Filtrem la llista de input
    return list(filter(lambda sample: sample['Accession'] in new_dict.values(), data))
