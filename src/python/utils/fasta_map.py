import time
from collections import namedtuple
from typing import Tuple, Dict, List, Iterable
from libs.seqalign import par_compare


class FastaMap:
    """
    Represents a Map that stores RNA codes
    """

    def __init__(self, arg):
        if isinstance(arg, str):
            self.__data = self._read(arg)
        elif isinstance(arg, Iterable):
            self.__data = dict(arg)
        else:
            raise TypeError("Invalid Argument")

    def __getitem__(self, rna_id):
        if rna_id not in self.__data:
            raise KeyError('Id not found')
        return self.__data[rna_id]

    def __iter__(self):
        for key, value in self.__data.items():
            yield key, value

    def keys(self):
        for key in self.__data.keys():
            yield key

    def values(self):
        for value in self.__data.values():
            yield value

    def filter(self, function):
        return FastaMap(filter(function, self))

    def _read(self, file_path: str) -> Dict[str, str]:
        """
        Reads a fasta file and returns a dict where the keys are the accessions
        and the values are the RNA sequences
        :param: file_path
        :return: sequences
        """
        data = dict()
        with open(file_path, 'r') as fasta:
            sequences = filter(None, fasta.read().split('>'))
            for seq in sequences:
                rna_id, rna = self._get_rna(seq)
                data[rna_id] = rna
        return data

    def build_hierarchy(self) -> Tuple[List[set]]:
        print("Grouping...")
        fr = time.time()
        ids = list(self.keys())
        to_compare = list()
        for i in range(len(ids) - 1):
            for j in range(i + 1, len(ids)):
                to_compare.append((ids[i], ids[j]))
        comparisons = par_compare(to_compare, self.__data)
        print(time.time() - fr)
        return comparisons

    @staticmethod
    def _get_rna(genome_info_str: str) -> Tuple[str, str]:
        """Get the header and the RNA from a String
        :param: A String that contains info about the genome
        :return: An Id-value tuple
        """
        lines = genome_info_str.split('\n')
        header, genome = lines[0], ''.join(lines[1:])
        genome_id = header.split('|')[0].strip()
        return genome_id, genome
