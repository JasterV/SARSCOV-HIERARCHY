from typing import Tuple, Dict, List, Union, Any
from utils.csv_table import CsvTable
import time
from pprint import pprint


class FastaMap:
    """Represents a Map that stores RNA codes
    Arguments: file_path: The path to the .fasta file -> String
    """

    def __init__(self, file_path):
        self.__data = self._read_fasta(file_path)

    def __getitem__(self, rna_id):
        if rna_id not in self.__data:
            raise KeyError('Id not found')
        return self.__data[rna_id]

    def _read_fasta(self, file_path: str) -> Dict[str, str]:
        """Reads a fasta file and returns a dict where the keys are the accessions
        and the values are the RNA sequences
        """
        data = dict()
        with open(file_path, 'r') as fasta:
            sequences = filter(None, fasta.read().split('>'))
            for seq in sequences:
                rna_id, rna = self._get_rna(seq)
                data[rna_id] = rna if len(rna) < 1000 else rna[:1000]
        return data

    def compare_samples(self, id1: str, id2: str) -> float:
        """Compares to rna codes
        Arguments: id1, id2 -> String
        return: float
        """
        s1, s2 = self[id1], self[id2]
        matrix = self._align_sequences(s1, s2)
        result = self._optimal_alignment(matrix, s1, s2)
        return result

    @staticmethod
    def _optimal_alignment(matrix, s1, s2, gap=-2):
        i, j = len(s1), len(s2)
        matches, length = 0, 0
        while (i > 0 or j > 0):
            if i > 0 and j > 0 and matrix[i][j] == matrix[i-1][j-1] + FastaMap.__is_match(s1[i - 1], s2[j - 1]):
                if s1[i - 1] == s2[j - 1]:
                    matches += 1
                i -= 1
                j -= 1
            elif i > 0 and matrix[i][j] == matrix[i-1][j] + gap:
                i -= 1
            else:
                j -= 1
            length += 1
        return matches / length

    @staticmethod
    def _align_sequences(s1, s2, gap=-2):
        s1_len, s2_len = len(s1), len(s2)
        matrix = [[0 for _ in range(s2_len + 1)] for _ in range(s1_len + 1)]
        for i in range(s1_len + 1):
            matrix[i][0] = gap * i
        for j in range(s2_len + 1):
            matrix[0][j] = gap * j
        for i in range(1, s1_len + 1):
            for j in range(1, s2_len + 1):
                match = matrix[i-1][j-1] + \
                    FastaMap.__is_match(s1[i - 1], s2[j - 1])
                delete = matrix[i - 1][j] + gap
                insert = matrix[i][j - 1] + gap
                matrix[i][j] = max(match, delete, insert)
        return matrix

    @staticmethod
    def __is_match(x, y, match=1, mismatch=-1):
        return match if x == y or x == 'N' or y == 'N' else mismatch

    @staticmethod
    def _get_rna(genome_info_str: str) -> Tuple[str, str]:
        """Get the header and the RNA from a String
        Argument: A String that contains info about the genome
        Return: An Id-value tuple
        """
        lines = genome_info_str.split('\n')
        header, genome = lines[0], ''.join(lines[1:])
        genome_id = header.split('|')[0].strip()
        return genome_id, genome

    def group_samples(self, csv_table: CsvTable) -> List[Union[set, Any]]:
        """Estructura del que pot ser la funció de creació de sets
        """
        star_time = time.time()
        compares = dict()
        list_relations = ()
        for i, sample_first in enumerate(csv_table):
            for sample_two in csv_table[1 + i:]:
                id1, id2 = sample_first['Accession'], sample_two['Accession']
                result = self.compare_samples(id1, id2)
                if result > 0.9:
                    compares.setdefault(id1, set())
                    compares[id1].add(id2)
        if compares:
            list_relations = self.generate_relations(compares)
        end_time = time.time() - star_time
        print(end_time)
        return list_relations

    @staticmethod
    def generate_relations(compares):
        list_relations = ()
        for elements in compares.keys():
            _, tree = FastaMap.explore_relations(compares, elements)
            if tree not in list_relations:
                list_relations = list_relations + (tree,)
        return list_relations

    @staticmethod
    def explore_relations(table, root, path=None, _sets=None):
        if _sets is None:
            _sets = set()
        if path is None:
            path = []
        path += [root]
        _sets.add(root)
        _sets.update(table.get(root, ""))
        for neighbor in table.get(root, ""):
            if neighbor not in path:
                path, _sets = FastaMap.explore_relations(
                    table, neighbor, path, _sets)
        return path, _sets
