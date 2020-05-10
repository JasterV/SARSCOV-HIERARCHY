from os.path import join
from sys import argv
from typing import Any, List, Union
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap


if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]

    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    fasta = FastaMap(fasta_path)
    csv_table = CsvTable(csv_path).filter()
    groups = fasta.group_samples(csv_table)
    print(groups)
