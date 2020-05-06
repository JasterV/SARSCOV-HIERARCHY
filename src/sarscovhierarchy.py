from os.path import join
from sys import argv
from typing import Any, List, Union
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap

#
# def group_samples(fasta: FastaMap, csv_table: CsvTable) -> List[Union[set, Any]]:
#     """Estructura del que pot ser la funció de creació de sets
#     """
#     # groups = list()
#     compares = dict()
#     for i, sample_first in enumerate(csv_table):
#         for sample_two in csv_table[1 + i:]:
#             id1, id2 = sample_first['Accession'], sample_two['Accession']
#             result = fasta.compare_samples(id1, id2)
#             if result > 0.7:
#                 compares.setdefault(id1, set())
#                 compares[id1].add(id2)
#
#     list_relations = generate_relations(compares)
#
#     return list_relations
#
#
# def generate_relations(compares):
#     list_relations = []
#     for elements in compares.keys():
#         _, tree = explore_relations(compares, elements)
#         if tree not in list_relations:
#             list_relations.append(tree)
#     return list_relations
#
#
# def explore_relations(table, root, path=None, _sets=None):
#     if _sets is None:
#         _sets = set()
#     if path is None:
#         path = []
#
#     path += [root]
#     _sets.add(root)
#     _sets.update(table.get(root, ""))
#     for neighbor in table.get(root, ""):
#         if neighbor not in path:
#             path, _sets = explore_relations(table, neighbor, path, _sets)
#
#     return path, _sets


if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]

    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    fasta = FastaMap(fasta_path)
    csv_table = CsvTable(csv_path).filter()
    
    print(csv_table)
