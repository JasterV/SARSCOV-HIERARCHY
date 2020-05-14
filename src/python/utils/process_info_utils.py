import psutil
import math
import sys
from os import environ, popen


def calcule_comparisons(n):
    result = 0
    for i in range(1, n):
        result += i
    return result


def get_mem_available():
    mem = psutil.virtual_memory()
    return mem.available / 1000000000


def get_num_system_cores():
    """ Returns the number of available threads on a posix/win based system """
    if sys.platform == 'win32':
        return int(environ['NUMBER_OF_PROCESSORS'])
    else:
        return int(popen('grep -c cores /proc/cpuinfo').read())


def get_max_threads(mem_available, mem_per_sample):
    threads_available = get_num_system_cores()
    num_threads = math.floor(mem_available/mem_per_sample)
    max_threads = num_threads if num_threads <= threads_available else threads_available
    return max_threads


def get_duration(num_threads, num_comparisons):
    comparison_duration = 3.5
    return ((num_comparisons*comparison_duration)/num_threads)/60


def get_max_mem_per_sample(max_sample_length):
    return ((max_sample_length**2)*2)/1000000000
