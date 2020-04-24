from os.path import join
from sys import argv, exit
from csv_utils import read_csv, country_dict, recur_country_dict
from fasta_utils import read_fasta

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]

    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    fasta_data = read_fasta(fasta_path)
    csv_data = read_csv(csv_path)

    medium = country_dict(csv_data)
    medium2 = recur_country_dict(csv_data)
    print(medium2)
