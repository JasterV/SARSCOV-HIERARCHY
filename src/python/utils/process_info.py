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
        Calculates system resources.
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
    def max_mem_per_comparison(self):
        return ((self.__max_sample_length ** 2) * 2) / 1000000000

    @property
    def mem_available(self):
        """
        :return memory available:
        """
        mem = psutil.virtual_memory()
        return mem.available / 1000000000

    @property
    def max_threads(self):
        threads_available = self.num_logic_cores if self.num_logic_cores <= 4 else 4
        threads = math.floor(self.mem_available / self.max_mem_per_comparison)
        max_threads = threads if threads <= threads_available else threads_available
        return max_threads if max_threads >= 1 else 1
