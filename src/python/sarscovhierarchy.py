from os.path import join
from sys import argv, exit

from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap
from utils.process_info_utils import *

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

    max_length = max(map(lambda x: int(x), csv_table.values("Length")))
    num_samples = len(fasta_map)


    num_comparisons = calcule_comparisons(num_samples)
    mem_available = get_mem_available()
    max_mem_per_sample = get_max_mem_per_sample(max_length)
    max_threads = get_max_threads(mem_available, max_mem_per_sample)
    # TODO: keyboard stop fix
    # TODO: restructure code
    print(
        f"\nThere are {num_samples} samples to compare in order to build the hierarchy.")
    print(
        f"So that means the program will need to perform {num_comparisons} comparisons!")
    print(
        "The algorithm implemented to compare 2 samples allocates a lot of memory (Up to {:.3f} GB of memory per comparison in the worst case)".format(
            max_mem_per_sample))
    print(
        "\nYour computer have {:.3f} GB's of memory available right now.".format(mem_available))
        
    result = list()
    if mem_available > 4:
        answer = input(
            "\nYou have the required space available to use multi-threading! Do you want to? (yes/no) ").strip().lower()
        while answer != "yes" and answer != "no":
            answer = input(
                "\nYou have the required space available to use multi-threading! Do you want to? (yes/no) ").strip().lower()
        if answer == "yes":
            print(
                f"\nThe maximum number of threads that can be used by the execution has been set to {max_threads}.")
            print("\nEstimated duration: {0:.3f} minutes.\n".format(
                get_duration(max_threads, num_comparisons)))
            result = fasta_map.build_hierarchy(f"{max_threads}")
        else:
            print("\nEstimated duration: {0:.3f} minutes.\n".format(
                get_duration(1, num_comparisons)))
            result = fasta_map.build_hierarchy("single")
    else:
        print("\nDue to the space available in your memory, you can't use multi-threading to perform the comparisons.")
        print("\nEstimated duration: {0:.3f} minutes.\n".format(
            get_duration(1, num_comparisons)))
        result = fasta_map.build_hierarchy("single")
    print(result)
