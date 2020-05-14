from sys import argv, exit
from os import environ, popen
from os.path import join
import sys
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap
import psutil
import math


def calcule_comparisons(n):
    result = 0
    for i in range(1, n):
        result += i
    return result


def get_mem_available():
    mem = psutil.virtual_memory()
    return mem.available / 1000000000


def get_threads():
    """ Returns the number of available threads on a posix/win based system """
    if sys.platform == 'win32':
        return int(environ['NUMBER_OF_PROCESSORS'])
    else:
        return int(popen('grep -c cores /proc/cpuinfo').read())


def get_max_threads(mem_available):
    threads_available = get_threads()
    num_threads = math.floor(mem_available/2)
    max_threads = num_threads if num_threads <= threads_available else threads_available
    return max_threads


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

    mem_available = get_mem_available()
    max_threads = get_max_threads(mem_available)
    num_samples = len(fasta_map)
    num_comparisons = calcule_comparisons(num_samples)

    print(
        f"\nThere are {num_samples} samples to compare in order to build the hierarchy.")
    print(
        f"So that means the program will need to perform {num_comparisons} comparisons!")
    print("The algorithm implemented to compare 2 samples allocates a lot of memory (Up to 2 GB of memory per comparison in the worst case)")

    answer = input(
        "\nDo you want to perform the comparisons using multi-threading? (Yes/No) ").strip().lower()
    while answer != "yes" and answer != "no":
        answer = input(
            "\nDo you want to perform the comparisons using multi-threading? (Yes/No) ").strip().lower()

    if answer == "yes":
        print(
            f"\nYou have {mem_available} GB available, so we set the maximum threads to {max_threads}!")
        fasta_map.build_hierarchy(f"{max_threads}")
    else:
        fasta_map.build_hierarchy("single")
