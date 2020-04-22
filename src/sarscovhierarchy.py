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
    """Reads a fasta file and returns a Map where the key are the accessions
    and the values are the RNA sequences
    """
    data = dict()
    with open(filepath, 'r') as fasta:
        sequences = fasta.read().strip().split('>')[1:]
        for seq in sequences:
            lines = seq.split('\n')
            seq_id = lines[0].split('|')[0].strip()
            data[seq_id] = ''.join(lines[1:])
    return data


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
