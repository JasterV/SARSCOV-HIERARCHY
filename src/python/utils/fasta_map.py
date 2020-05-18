"""
    Module prepared for the comparison of samples from our FASTA
    document and the creation of a hierarchy.
    Some of the lower level functions are
    performed with a connection to Rust.
"""

import collections
import time
from typing import Tuple, Dict, List, Callable

import libs.seqalign as sq


class FastaMap:
    """
    Represents a Map that stores RNA codes
    """

    def __init__(self, arg):
        if isinstance(arg, str):
            self.__data = self._read(arg)
        elif isinstance(arg, collections.Iterable):
            self.__data = dict(arg)
        else:
            raise TypeError("Invalid Argument")

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, rna_id):
        if rna_id not in self.__data:
            raise KeyError('Id not found')
        return self.__data[rna_id]

    def __iter__(self):
        for key, value in self.__data.items():
            yield key, value

    # TODO: key and values function review
    def keys(self):
        """
        :return Generator of keys
        """
        for key in self.__data.keys():
            yield key

    def values(self):
        """
        :return Generator of values:
        """
        for value in self.__data.values():
            yield value

    # TODO: review filter function, classmethod
    def filter(self, function: Callable):
        """
        Create a new instance of FastaMap with new values
        :param function:
        :return:
        """
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

    def build_hierarchy(self, threads_option) -> Tuple[List[set]]:
        """
        The function that is in charge of the comparison and the hierarchy of the samples
        :param threads_option:
        :return:
        """
        print("Performing comparisons...")
        start_time = time.time()
        ids = list(self.keys())
        to_compare = list()
        for i in range(len(ids) - 1):
            for j in range(i + 1, len(ids)):
                to_compare.append((ids[i], ids[j]))
        comparisons = sq.par_compare(to_compare, self.__data, threads_option)
        print(f"Comparisons performed in {time.time() - start_time} seconds!")
        return comparisons

    @staticmethod
    def _get_rna(genome_info_str: str) -> Tuple[str, str]:
        """
        Get the header and the RNA from a String
        :param A String that contains info about the genome:
        :return An Id-value tuple:
        """
        lines = genome_info_str.split('\n')
        header, genome = lines[0], ''.join(lines[1:])
        genome_id = header.split('|')[0].strip()
        return genome_id, genome
