from os.path import join
from sys import argv, exit
from utils.csv_utils import read_csv, filter_country_average_length
from utils.fasta_utils import Fasta

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]

    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    fasta = Fasta(fasta_path)
    csv_data = read_csv(csv_path)

    filtered_data = filter_country_average_length(csv_data)

    id1 = filtered_data[0]['Accession']
    id2 = filtered_data[1]['Accession']
    result = fasta.compare_rna(id1, id2)
    print(result)