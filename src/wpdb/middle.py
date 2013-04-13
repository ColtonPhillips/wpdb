class Cruncher(object):
	"""
	A Cruncher has a list of functions that are used to analyze, 
	compute, parse, the xml of the object, or otherwise do
	any arbitrary calls. These functions return strings that are
	used as the columns for the csv file
	"""
	def __init__(self, xml=None):
		self.xml = xml
		self.crunches = []

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

	def to_csv_line(self):
		print ''