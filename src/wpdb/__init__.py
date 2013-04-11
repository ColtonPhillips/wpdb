# from wpdb import * will import the following
__all__ = ['wpdb', 'debug', 'wikiurl']

# importing wpdb imports all associated sub-modules as well
import debug, wikiurl

# we want all of  our core functions over at wpdb.py
from wpdb import *