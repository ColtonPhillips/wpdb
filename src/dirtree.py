import string

#It irks me greatly how my dir is just as useless as dir right now. sasuke it all away.

def _dirt_recurse(module, verbose=False, file=False, tab_width=0):
    list = dir(module)
    if file:
        # TODO: put that shit in a file
        pass
    else:
        for item in list:
            if item.startswith("__") and not verbose:
                pass
            else:
                #TODO: I'll need to rethink the recursive stuff when i can actually get a hook on when to stop recursing _ CP
                print "|" + ("-" * tab_width) + "> " + item
                # FUUCK IT ILL JUST LIMIT IT AT LIKE 2 OR WHATEVER
                # Pretty fucking useless, but serves as a demonstration
                #if tab_width < 2:
                #   __dirt_recurse__(item,verbose,file,tab_width+1)
                 
def dirt(module, verbose=False, file=False):
    _dirt_recurse(module, verbose, file)