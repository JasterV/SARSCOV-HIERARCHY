from os.path import join
from sys import argv, exit
from src.utils.csv_utils import read_csv, country_dict
from src.utils.fasta_utils import read_fasta

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]

    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    fasta_data = read_fasta(fasta_path)
    csv_data = read_csv(csv_path)

    ctry_dict = country_dict(csv_data)
