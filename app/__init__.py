import os

def math(a, new_b):
    """
    This is useless math
    :param a: number
    :param new_b: number
    :return: number
    """
    if a < new_b:
        return a + new_b
    if new_b == a or new_b > 10:
        return a
    else:
        return new_b
