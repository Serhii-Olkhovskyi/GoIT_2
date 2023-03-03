from time import time
from multiprocessing import *
from loguru import logger

timer = time()

numbers = [128, 255, 99999, 10651060]


def factorize(numbers):
    all_num = []
    for num in numbers:
        all_num.append(div(num))
    return all_num


def div(num):
    del_n = []
    for i in range(1, num + 1):
        if num % i == 0:
            del_n.append(i)
    return del_n


if __name__ == "__main__":

    a, b, c, d = factorize(numbers)

    logger.info(f'Done by function for: {round(time() - timer, 4)}')

    logger.info(f"Count CPU: {cpu_count()}")

    with Pool(cpu_count()) as p:
        p.map_async(div, numbers)

    logger.info(f'Done by pool for: {round(time() - timer, 4)}')
