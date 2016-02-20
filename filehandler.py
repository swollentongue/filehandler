import os
import csv
import openpyxl
from argparse import ArgumentParser
import pandas as pd

class FileHandlerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UniversalFile(object):
    '''
    info tk
    '''

    extension_list = ('xls', 'xlsx', 'txt', 'csv')

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        return self

class TxtHandler(UniversalFile):
    def __init__(self, filename):
        UniversalFile.__init__(self, filename)
        try:
            self.base_file = open(filename, 'rU')
        except IOError:
            raise FileHandlerError('File error. Please make sure you types the correct filename.')

    def next(self):
        try:
            line = self.base_file.next()
            return line.strip().split('\t')
        except StopIteration:
            self.base_file.seek(0)
            raise StopIteration

class CSVHandler(UniversalFile):
    def __init__(self, filename):
        UniversalFile.__init__(self, filename)
        try:
            self.flat_file = open(filename, 'r')
            self.base_file = csv.reader(self.flat_file)
        except IOError:
            raise FileHandlerError('File error. Please make sure you types the correct filename.')

    def next(self):
        try:
            return self.base_file.next()
        except StopIteration:
            self.flat_file.seek(0)
            raise StopIteration

class ExcelHandler(UniversalFile):
    def __init__(self, filename, header_row = None):
        UniversalFile.__init__(self, filename)
        try:
            self.data_frame = pd.read_excel(filename, header=header_row)
            cols = sheet.columns.values
            self.base_file = (tuple(x) for x in subset.values)
        except IOError:
            raise FileHandlerError('File error. Please make sure you types the correct filename.')

    def next(self):
        try:
            return self.base_file.next()
        except StopIteration:
            self.base_file = (tuple(x) for x in subset.values)
            raise StopIteration

# class FileHandler()


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("input", type=str, help="File to input.")
    args = argparser.parse_args()
    f = CSVHandler(args.input)
    for line in f:
        print line
