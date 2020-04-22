from sys import argv, exit
from csv import DictReader
from os.path import join


def read_csv(filepath):
    """Reads a csv file and returns a list of Ordered Maps
    """
    with open(filepath, 'r') as csv_file:
        reader = DictReader(csv_file, delimiter=',')
        return list(reader)

def read_fasta(filepath):
    """Reads a fasta file
    TODO: Clear the data
    """
    with open(filepath, 'r') as fasta:
        return fasta.read().split('>')


if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]
    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")
    # Read files
    fasta_data = read_fasta(fasta_path)
    csv_data = read_csv(csv_path)