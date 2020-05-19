import os
import signal
from os.path import join
from sys import argv

import utils.process_info_utils as piu
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap


def show_system_info(samples, comparisons, mem_per_sample, available):
    print(
        f"\nThere are {samples} samples to compare in order to build the hierarchy.")
    print(
        f"So that means the program will need to perform {comparisons} comparisons!")
    print(
        "The algorithm implemented to compare 2 samples allocates "
        "a lot of memory (Up to {:.3f} GB of memory per "
        "comparison in the worst case)".format(
            mem_per_sample))
    print(
        "\nYour computer have {:.3f} GB's of memory available right now.".format(available))


def sequence_decision(available_mam, threads_max, comparisons_num, fasta):
    if available_mam > 4:
        answer = input(
            "\nYou have the required space available to use "
            "multi-threading! Do you want to? (yes/no) ").strip().lower()
        while answer not in ('yes', 'no'):
            answer = input(
                "\nYou have the required space available to "
                "use multi-threading! Do you want to? (yes/no) ").strip().lower()
        if answer == "yes":
            print(
                f"\nThe maximum number of threads that can be "
                f"used by the execution has been set to {threads_max}.")
            return estimated_duration(threads_max, comparisons_num, fasta)
        return estimated_duration(threads_max, comparisons_num, fasta)
    print("\nDue to the space available in your memory,"
          " you can't use multi-threading to perform the comparisons.")
    return estimated_duration(1, comparisons_num, fasta)


def estimated_duration(threads, comparisons, fasta_map):
    print("\nEstimated duration: {0:.3f} minutes.\n".format(
        piu.get_duration(threads, comparisons)))
    if threads > 1:
        return fasta_map.build_hierarchy(f"{threads}")
    return fasta_map.build_hierarchy("single")


def run():
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
    num_comparisons = piu.calcule_comparisons(num_samples)
    mem_available = piu.get_mem_available()
    max_mem_per_sample = piu.get_max_mem_per_sample(max_length)
    max_threads = piu.get_max_threads(mem_available, max_mem_per_sample)
    show_system_info(num_samples,
                     num_comparisons,
                     max_mem_per_sample,
                     mem_available)
    result = sequence_decision(mem_available,
                               max_threads,
                               num_comparisons, fasta_map)
    print(result)


if __name__ == '__main__':
    if len(argv) == 2:
        pid = os.getpid()
        pid_h = os.fork()
        if pid_h == 0:
            run()
        else:
            try:
                os.wait()
            except KeyboardInterrupt:
                os.kill(pid_h, signal.SIGKILL)
                print("shutdown")
    else:
        print("python sarscovhierarchy.py <directory>")
