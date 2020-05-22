"""
    Module prepared for the comparison of samples from our FASTA
    document and the creation of a hierarchy.
    Some of the lower level functions are
    performed with a connection to Rust.
"""
import collections
import time
from typing import Tuple, Dict, Callable

import libs.seqalign as sq

from utils.process_info import ProcessInfo


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

    def filter(self, function: Callable):
        """
        Create a new instance of FastaMap with new values
        :param function:
        :return:
        """
        return FastaMap(filter(function, self))

    def compare_all_samples(self):
        """
        The function that is in charge of the comparison and the hierarchy of the samples
        :return None:
        """
        comparisons = self._compare_all_samples()
        table = self._to_dict(comparisons)
        return table

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

    def _compare_all_samples(self):
        # Calculate the number of threads that can be
        # used in order to speed up the comparisons
        max_length = max(map(len, self.__data.values()))
        num_samples = len(self.__data)
        threads = ProcessInfo(num_samples, max_length).max_threads
        # Start the comparisons
        print("Performing comparisons...")
        start_time = time.time()
        ids = list(self.__data.keys())
        to_compare = [(ids[i], ids[j])
                      for i in range(len(ids) - 1)
                      for j in range(i + 1, len(ids))]
        comparisons = sq.par_compare(to_compare, self.__data, str(threads))
        print(
            f"Comparisons performed in {time.time() - start_time:.3f} seconds!")
        return comparisons

    @staticmethod
    def _to_dict(comparisons):
        sample_compare = dict()
        for id1, id2, distance in comparisons:
            sample_compare.setdefault(id1, dict())[id2] = distance
            sample_compare.setdefault(id2, dict())[id1] = distance
        return sample_compare

    @staticmethod
    def _get_rna(genome_info_str: str) -> Tuple[str, str]:
        """
        Get the header and the RNA from a String
        :param A String that contains info about the genome:
        :return An Id-value tuple:
        """
        lines = genome_info_str.split('\n')
        header, genome = lines[0], ''.join(lines[1:])
        genome_id = header.split('|')[0].strip().split(".")[0]
        return genome_id, genome
