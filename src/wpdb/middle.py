from bs4 import BeautifulSoup
import csv

class Cruncher(object):
	"""
	A Cruncher has a list of functions that are used to analyze, 
	compute, parse, the xml of the object, or otherwise do
	any arbitrary calls.
	"""
	def __init__(self, crunches=[], xml=None):
		self.xml = xml
		self.soup = BeautifulSoup(xml,'lxml')
		self.crunches = crunches
		self.result = []

		self.crunch_data = {
				'xml': self.xml,
				'soup': self.soup,
				'title': self.soup.find('page')['title']
		}

		self.crunch()

	def addFunction(self, new_function):
		"""
		Add a single function to the crunch list
		"""
		self.crunches.append(new_function)

	def addFunctions(self, new_functions):
		"""
		Add a list of functions to the crunch list
		"""
		self.crunches.extend(new_functions)

	def crunch(self):
		self.result = []
		for fun in self.crunches:
			self.result.append(fun(self.crunch_data))
