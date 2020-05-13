import time
from collections import namedtuple
from multiprocessing.dummy import Pool
from typing import Tuple, Dict, List

import libs.seqalign as sq

from utils.csv_table import CsvTable


class FastaMap:
    """
    Represents a Map that stores RNA codes
    Arguments: file_path: The path to the .fasta file -> String
    """

    def __init__(self, file_path):
        self.__data = self._read_fasta(file_path)

    def __getitem__(self, rna_id):
        if rna_id not in self.__data:
            raise KeyError('Id not found')
        return self.__data[rna_id]

    def _read_fasta(self, file_path: str) -> Dict[str, str]:
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

    def group_samples(self, csv_table: CsvTable) -> Tuple[List[set]]:
        """
        Creation Sets "family samples"
        :param: csv_table:
        :return: tuple of relations
        """
        print("Grouping...")
        fr = time.time()
        to_compare = [(sample_first['Accession'], sample_two['Accession'])
                      for i, sample_first in enumerate(csv_table)
                      for sample_two in csv_table[i + 1:]]
        compares = dict()
        p = Pool()
        results = p.map(self.compare_multi, to_compare)
        for x in results:
            compares.setdefault(x.id1, set())
            compares[x.id1].add(x.id2)
        print(time.time() - fr)

    def compare_multi(self, ids: tuple) -> Tuple[str, str, float]:
        """
        Function to parallelize comparisons
        :param ids :
        :return: Tuple of relations
        """
        named_compare = namedtuple("comparator", "id1 id2 result")
        s1, s2 = self[ids[0]], self[ids[1]]
        result = sq.needleman_wunsch(s1, s2)
        return named_compare(ids[0], ids[1], result)
