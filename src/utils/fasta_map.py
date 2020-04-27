import concurrent.futures
from collections import namedtuple
from typing import Tuple, Dict, List, Union, Any

from utils.csv_table import CsvTable


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

    def compare_samples(self, id1, id2):
        """Compares to rna codes
        Arguments: id1, id2 -> String
        return: float
        """
        rna1, rna2 = self[id1], self[id2]
        len1, len2 = len(rna1), len(rna2)
        matches = 0
        for i in range(min(len1, len2)):
            symbol1, symbol2 = rna1[i], rna2[i]
            if symbol1 == symbol2 or symbol1 == 'N' or symbol2 == 'N':
                matches += 1
        return matches / max(len1, len2)

    def _read_fasta(self, file_path: str) -> Dict[str, str]:
        """Reads a fasta file and returns a dict where the keys are the accessions
        and the values are the RNA sequences
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

        to_compare = []
        compares = dict()
        for i, sample_first in enumerate(csv_table):
            for sample_two in csv_table[1 + i:]:
                id1, id2 = sample_first['Accession'], sample_two['Accession']
                to_compare.append((id1, id2))
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.compare_multi, to_compare)
        print(results)
        for x in results:
            compares.setdefault(x.id1, set())
            compares[x.id1].add(x.id2)
        list_relations = FastaMap.generate_relations(compares)

        return list_relations

    def compare_multi(self, ids):
        named_compare = namedtuple("comparation", "id1 id2")
        result = self.compare_samples(ids[0], ids[1])
        if result > 0.9:
            r = named_compare(ids[0], ids[1])
        print(r)
        return r

    @staticmethod
    def generate_relations(compares):
        list_relations = []
        for elements in compares.keys():
            _, tree = FastaMap.explore_relations(compares, elements)
            if tree not in list_relations:
                list_relations.append(tree)
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
                path, _sets = FastaMap.explore_relations(table, neighbor, path, _sets)

        return path, _sets
