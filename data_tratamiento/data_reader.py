import sys
from csv import DictReader
from typing import Tuple, List, Dict, Iterator, Any, Union

sys.setrecursionlimit(10 ** 6)


def get_rna(genome_info_str: str) -> Tuple[str, str]:
    """Get the header and the RNA from a String
    Argument: A String that contains info about the genome
    Return: An Id-value tuple
    """
    lines: List[str] = genome_info_str.split('\n')
    header, genome = lines[0], ''.join(lines[1:])
    genome_id: str = header.split('|')[0].strip()
    return genome_id, genome


def read_fasta(file_path: str) -> Dict[str, str]:
    """Reads a fasta file and returns a dict where the keys are the accessions
    and the values are the RNA sequences
    """
    data = dict()
    with open(file_path, 'r') as fasta:
        sequences: Iterator[str] = filter(None, fasta.read().split('>'))
        for seq in sequences:
            rna_id, rna = get_rna(seq)
            data[rna_id]: str = rna
    return data


def read_csv(file_path: str) -> List:
    """Reads a csv file and returns a list of Ordered Maps
    """
    with open(file_path, 'r') as csv_file:
        reader: DictReader = DictReader(csv_file, delimiter=',')
        return list(reader)


def country_dict(csv_data: List[Dict]) -> Dict:
    """
    calculate the average length of regions
    :param csv_data: A csv with the regions
    :return: Dictionary with the average length
    """
    countries = dict()
    for test in csv_data:
        location: Union[str, Any] = test.get("Geo_Location", " ")
        if location not in countries:
            numbers: Iterator[Dict] = filter(lambda x: x["Geo_Location"] == location, csv_data)
            countries[location] = sorted(list(x.get("Length") for x in numbers))
    return {c: countries[c][len(countries[c]) // 2] for c in countries}


# TODO: modify sorted, only if it is necessary.

def recur_country_dict(csv_data, countries=None):
    if countries is None:
        countries = dict()
    if not csv_data:
        return {c: countries[c][len(countries[c]) // 2] for c in countries}
    location = csv_data[0]["Geo_Location"]
    if location not in countries:
        numbers = filter(lambda x: x["Geo_Location"] == location, csv_data)
        countries[location] = sorted(list(x.get("Length") for x in numbers))
    return recur_country_dict(csv_data[1:], countries)
