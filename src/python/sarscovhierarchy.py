import signal
import os
from os.path import join
from sys import argv, exit

from utils.process_info_utils import ProcessInfo
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap


def ask(question):
    answer = input(f"{question} (yes/no) ").strip().lower()
    while answer not in ('yes', 'no'):
        answer = input(f"\n{question} (yes/no) ").strip().lower()
    return answer


def check_threading(available_mem, max_threads):
    if available_mem > 4:
        answer = ask(
            "You have the required space available to use multi-threading! Do you want to?")
        if answer == 'yes':
            print(
                f"\nThe maximum number of threads that can be "
                f"used by the execution has been set to {max_threads}.")
            return max_threads
    return 1


def build_hierarchy(fasta, piu):
    threads = check_threading(piu.mem_available, piu.max_threads)
    print("\nEstimated duration: {0:.3f} minutes.\n".format(
        piu.estimated_duration(threads, piu.num_comparisons)))
    threads_option = str(threads) if threads > 1 else "single"
    fasta.build_hierarchy(threads_option)

signal.signal(signal.SIGTSTP, signal.SIG_IGN)

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <data_path>")
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

    piu = ProcessInfo(num_samples, max_length)
    piu.show_system_info()

    try:
        pid_h = os.fork()
        if pid_h == 0:
            build_hierarchy(fasta_map, piu)
            exit(0)
        os.wait()
    except KeyboardInterrupt:
        os.kill(pid_h, signal.SIGKILL)
        print("Bye!")
    except:
        print("Unexpected Error")
