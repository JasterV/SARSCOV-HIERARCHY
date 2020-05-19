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
        self.__samples = num_samples
        self.__num_comparisons = self.__cal_comparisons(num_samples)
        self.__mem_available = self.__get_mem_available()
        self.__max_mem_per_sample = self.__get_max_mem_per_sample(max_length)
        self.__max_threads = self.__get_max_threads(
            self.__mem_available, self.__max_mem_per_sample)

    @property
    def num_comparisons(self):
        """
        :return num of comparisons:
        """
        return self.__num_comparisons

    @property
    def max_threads(self):
        """
        :return num max of threads:
        """
        return self.__max_threads

    @property
    def mem_available(self):
        """
        :return memory available:
        """
        return self.__mem_available

    @staticmethod
    def estimated_duration(num_threads, num_comparisons):
        """
        :param num_threads:
        :param num_comparisons:
        :return estimated time execution in minutes:
        """
        comparison_duration = 3.5
        return ((num_comparisons * comparison_duration) / num_threads) / 60

    def show_system_info(self):
        """
           Show information
        """
        print(
            f"\nThere are {self.__samples} samples to compare in order to build the hierarchy.")
        print(f"So that means the program will need "
              f"to perform {self.__num_comparisons} comparisons!")
        print("The algorithm implemented to compare 2 samples allocates "
              "a lot of memory (Up to {:.3f} GB of memory per "
              "comparison in the worst case)".format(self.__max_mem_per_sample))
        print("\nYour computer have {:.3f} GB's "
              "of memory available right now.".format(self.__mem_available))

    @staticmethod
    def __cal_comparisons(max_number):
        """
        :param max_number:
        :return sum of comparisons:
        """
        return sum(range(1, max_number))

    @staticmethod
    def __get_mem_available():
        mem = psutil.virtual_memory()
        return mem.available / 1000000000

    @staticmethod
    def __get_num_system_cores():
        """ Returns the number of available threads on a posix/win based system """
        if sys.platform == 'win32':
            return int(environ['NUMBER_OF_PROCESSORS'])
        return int(popen('grep -c cores /proc/cpuinfo').read())

    def __get_max_threads(self, mem_available, mem_per_sample):
        threads_available = self.__get_num_system_cores()
        threads = math.floor(mem_available / mem_per_sample)
        max_threads = threads if threads <= threads_available else threads_available
        return max_threads

    @staticmethod
    def __get_max_mem_per_sample(max_sample_length):
        return ((max_sample_length ** 2) * 2) / 1000000000
