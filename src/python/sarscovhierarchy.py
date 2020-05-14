from sys import argv, exit
from os.path import join
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap

def calcule_comparisons(n):
    result = 0
    for i in range(1, n + 1):
        result += i
    return result

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]
    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    print("Reading and processing files...")
    csv_table = CsvTable(csv_path) \
        .group_countries_by_median_length()
    ids = csv_table.values('Accession')
    fasta_map = FastaMap(fasta_path) \
        .filter(lambda item: item[0] in ids)
    print("Files processing finished!")

    num_samples = len(fasta_map)
    num_comparisons = calcule_comparisons(num_samples)

    print(f"\nThere are {num_samples} samples to compare in order to build the hierarchy.")
    print(f"So that means the program will need to perform {num_comparisons} comparisons!")
    print("The algorithm implemented to compare 2 samples allocates a lot of memory (Up to 2 GB of memory per comparison in the worst case)")

    answer = input("\nDo you want to perform the comparisons using multi-threading? (Yes/No) ").strip().lower()
    while answer != "yes" and answer != "no":
        answer = input("\nDo you want to perform the comparisons using multi-threading? (Yes/No) ").strip().lower()

    if answer == "yes":
        print("\nWARNING!! THE PROCESS CAN FAIL IF YOUR COMPUTER DOES NOT HAVE THE REQUIRED AMOUNT OF MEMORY TO PERFORM THIS EXECUTION")
        answer = input("\nAre you sure? (Yes/No) ").strip().lower()
        while answer != "yes" and answer != "no":
            answer = input("\nAre you sure? (Yes/No) ").strip().lower()
        if answer == "yes":
            threads = input("\nHow many threads do you want to use? Choose 'unlimited' if you dont care about the maximum threads: ").strip().lower()
            while not threads.isnumeric() and threads != "unlimited":
                threads = input("\nHow many threads do you want to use? Choose 'unlimited' if you dont care about the maximum threads: ").strip().lower()
                if threads.isnumeric() and int(threads) < 2:
                    print("\nYou've chosen multi-threading, can't choose less than 2 threads now")
                    threads = " "           
            fasta_map.build_hierarchy(threads)
        else:
            fasta_map.build_hierarchy("single")
    else:
        fasta_map.build_hierarchy("single")


