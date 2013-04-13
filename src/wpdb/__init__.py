# from wpdb import * will import the following
__all__ = ['wpdb', 'debug', 'front', 'middle', 'back']

# importing wpdb imports all associated sub-modules as well
import debug, front, middle, back

# we want all of  our core functions over at wpdb.py
from wpdb import *