"""Ultility and helper functions"""
import csv

# Prettify exception
import sys
sys.tracebacklimit = 0


def read_file(file_path, file_name):
    """Read file to python list"""
    information = []
    with open(f"{file_path}\\{file_name}.csv") as file:
        reader = csv.DictReader(file)
        for _ in reader:
            information.append(_)
    return information


def write_file(file_path, file_name='reports', extension='txt', data=''):
    """Write file to custom directory"""
    with open(f"{file_path}\\{file_name}.{extension}", "w+") as file:
        file.write(data)
