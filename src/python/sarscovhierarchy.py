from sys import argv, exit
from os.path import join
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]
    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")
    # READ AND FILTER CSV
    csv_table = CsvTable(csv_path) \
        .group_countries_by_median_length()
    # GET ALL THE SAMPLE ACCESSIONS
    ids = csv_table.values('Accession')
    # READ AND FILTER FASTA
    fasta_map = FastaMap(fasta_path) \
        .filter(lambda item: item[0] in ids)
    # TEST COMPARISONS SPEED
    d = fasta_map.build_hierarchy()
    print(len(d))
    print(d)
