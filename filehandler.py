import os
import csv
import codecs
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
    def __init__(self, filename):
        try:
            self.base_file = codecs.open(filename, 'r', 'utf-8')
        except IOError:
            raise FileHandlerError('File error. Please make sure you types the correct filename.')

    def __iter__(self):
        return self

class TxtHandler(UniversalFile):
    def next(self):
        try:
            return self.base_file.next().strip().split('\t')
        except StopIteration:
            self.base_file.seek(0)
            raise StopIteration

class CSVHandler(UniversalFile):
    def __init__(self, filename):
        UniversalFile.__init__(self, filename)
        self.csv_file = csv.reader(self.base_file)

    def next(self):
        try:
            return self.csv_file.next()
        except StopIteration:
            self.base_file.seek(0)
            raise StopIteration

class ExcelHandler(UniversalFile):
    def __init__(self, filename, header_row = None):
        try:
            self.data_frame = pd.read_excel(filename, header=header_row)
            self.set_file()
        except IOError:
            raise FileHandlerError('File error. Please make sure you types the correct filename.')

    def next(self):
        try:
            return list(self.base_file.next())
        except StopIteration:
            self.set_file()
            raise StopIteration

    def set_file(self):
        self.base_file = (tuple(x) for x in self.data_frame.to_records(index=False))

def FileHandler(filename):
    extension_list = ('xls', 'xlsx', 'txt', 'csv')
    file_extension = filename.split('.')[-1]
    if file_extension in extension_list:
        if file_extension == 'txt':
            return TxtHandler(filename)
        elif file_extension == 'csv':
            return CSVHandler(filename)
        else:
            return ExcelHandler(filename)
    else:
        raise FileHandlerError('File type unsupported.')


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("input", type=str, help="File to input.")
    args = argparser.parse_args()
    f = FileHandler(args.input)
    for line in f:
        print line
