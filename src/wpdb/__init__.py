# from wpdb import * will import the following
__all__ = ['wpdb', 'debug', 'wikiurl', 'dummy']

# importing wpdb imports all associated sub-modules as well
import debug, wikiurl, dummy