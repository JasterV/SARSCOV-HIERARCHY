from os.path import join
from sys import argv
from typing import Any, List, Union
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap


if len(argv) != 2:
    print("python sarscovhierarchy.py <directory>")
    exit()
data_dir = argv[1]

csv_path = join(data_dir, "sequences.csv")
fasta_path = join(data_dir, "sequences.fasta")

fasta = FastaMap(fasta_path)
csv_table = CsvTable(csv_path).filter()
id1, id2 = csv_table[0]['Accession'], csv_table[1]['Accession']
groups = fasta.group_samples(csv_table)
print(groups)
