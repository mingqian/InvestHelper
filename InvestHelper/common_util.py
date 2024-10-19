import queue
from datetime import datetime as dt

event_queue = queue.Queue()

def compare_date_str(x, y) -> bool:
    """
    For date string x, y,
    returns True if x > y
    else False
    """
    a = dt.strptime(x, '%Y-%m-%d')
    b = dt.strptime(y, '%Y-%m-%d')
    return a > b


def neg_float_str(x) -> str:
    """
    For string x of a float,
    returns a string of the minus float
    """
    try:
        return str(-abs(float(x)))
    except TypeError:
        print('neg_float_str: conversion error')
        return "-1"
