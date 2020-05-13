import time
from collections import namedtuple
from multiprocessing.dummy import Pool
from typing import Tuple, Dict, List, Iterable

import libs.seqalign as sq


class FastaMap:
    """
    Represents a Map that stores RNA codes
    Arguments: file_path: The path to the .fasta file -> String
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

    def group_samples(self) -> Tuple[List[set]]:
        """
        Creation Sets "family samples"
        :return: tuple of relations
        """
        print("Grouping...")
        p = Pool()
        fr = time.time()
        comparisons = dict()
        ids = list(self.keys())

        to_compare = [(ids[i], ids[i + 1]) for i in range(len(ids) - 1)]
        results = p.map(self.compare_samples, to_compare)
        for x in results:
            id1, id2, result = x[0], x[1], x[2]
            comparisons.setdefault(id1, dict())[id2] = result 
            comparisons.setdefault(id2, dict())[id1] = result 
        print(time.time() - fr)
        return comparisons

    def compare_samples(self, ids: tuple) -> Tuple[str, str, float]:
        """
        Function to parallelize comparisons
        :param ids :
        :return: Tuple of relations
        """
        s1, s2 = self[ids[0]], self[ids[1]]
        result = sq.needleman_wunsch(s1, s2)
        return (ids[0], ids[1], result)
