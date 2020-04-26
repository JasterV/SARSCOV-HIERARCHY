from os.path import join
from sys import argv, exit
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap
from typing import List


def group_samples(fasta: FastaMap, csv_table: CsvTable) -> List[set]:
    """Estructura del que pot ser la funció de creació de sets
    """
    groups = list()
    for i in range(len(csv_table) - 1):
        for j in range(i + 1, len(csv_table)):
            id1, id2 = csv_table[i]['Accession'], csv_table[j]['Accession']
            result = fasta.compare_samples(id1, id2)
            if result > 0.7:
                pass
                #add_ids(groups, id1, id2)
    return groups


if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]

    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    fasta = FastaMap(fasta_path)
    csv_table = CsvTable(csv_path).filter()

    groups = group_samples(fasta, csv_table)
    print(groups)

