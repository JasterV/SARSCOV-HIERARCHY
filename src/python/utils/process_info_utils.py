"""
    Module for ProcessInfo class in charge of
    managing the information of the system
    and the execution
"""
import math
import sys
from os import environ, popen

import psutil


class ProcessInfo:
    """
        informer and delimiter of system resources.
    """

    def __init__(self, num_samples, max_length):
        self.__num_samples = num_samples
        self.__max_sample_length = max_length

    @property
    def num_logic_cores(self):
        """ Returns the number of available threads on a posix/win based system """
        if sys.platform == 'win32':
            return int(environ['NUMBER_OF_PROCESSORS'])
        return int(popen('grep -c cores /proc/cpuinfo').read())

    @property
    def max_mem_per_sample(self):
        return ((self.__max_sample_length ** 2) * 2) / 1000000000

    @property
    def max_threads(self):
        threads_available = self.num_logic_cores
        threads = math.floor(self.mem_available / self.max_mem_per_sample)
        max_threads = threads if threads <= threads_available else threads_available
        return max_threads

    @property
    def num_comparisons(self):
        """
        :return num of comparisons:
        """
        return sum(range(1, self.__num_samples))

    @property
    def mem_available(self):
        """
        :return memory available:
        """
        mem = psutil.virtual_memory()
        return mem.available / 1000000000

    def estimated_duration(self, num_threads):
        """
        :param num_threads:
        :param num_comparisons:
        :return estimated time execution in minutes:
        """
        comparison_duration = 3.5
        return ((self.num_comparisons * comparison_duration) / num_threads) / 60

    def show_system_info(self):
        """
           Show information
        """
        print(
            f"\nThere are {self.__num_samples} samples to compare in order to build the hierarchy.")
        print(f"So that means the program will need "
              f"to perform {self.num_comparisons} comparisons!")
        print("The algorithm implemented to compare 2 samples allocates "
              "a lot of memory (Up to {:.3f} GB of memory per "
              "comparison in the worst case)".format(self.max_mem_per_sample))
        print("\nYour computer have {:.3f} GB's "
              "of memory available right now.".format(self.mem_available))

