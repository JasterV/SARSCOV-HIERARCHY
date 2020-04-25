from os.path import join
from sys import argv, exit

from utils.csv_utils import CSV
from utils.fasta_utils import Fasta

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]

    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    fasta = Fasta(fasta_path)
    csv_data = CSV(csv_path=csv_path).filter()
