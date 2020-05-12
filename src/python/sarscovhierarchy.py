from os.path import join
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap

if __name__ == '__main__':
    data_dir = "./data"
    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")
    fasta = FastaMap(fasta_path)
    csv_table = CsvTable(csv_path).filter()
    print(csv_table)

