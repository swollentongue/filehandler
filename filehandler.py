import os
import csv
import 

class FileHandlerError(Exception):
    def __init__(self, value):
        self.value = value
	def __str__(self):
		return repr(self.value)

class FileHandler(class):
	'''
	class to handle multiple file types
	usage f = FileHandler('/path/to/file/filename')
	'''

	self.extension_list = ('xls', 'xlsx', 'txt', 'csv')

	def __init__(self, filename):
		self.filename = filename
		filename_path = os.path.split(filename)[0]
		if filename_path != '':
			self.path = filename_path
		else:
			self.path = os.getcwd()


	def open_file(self):
		extension = self.filename.split('.')[-1]
		if self.extension in self.extension_list:

