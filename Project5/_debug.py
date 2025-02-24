###################################################################################
# Debug Class
# - debug class made to help debug code w/out an abhorent amount of print
#   statements
#
#
#
###################################################################################
# Things to check:
#   - var types and returns of our init vars and arrays
#   - Check why propogating wave twice works (maybe the first few time steps?)
#   - Make sure our array is working the way it needs to

#Import libs
from matplotlib import pyplot as plt

class debug:
    #Lets us know if we need to actually run the values
    def __init__(self,debug:bool):
        self.debug_mode = debug

    def print(self,values:object,statement:str = "",):
        if self.debug_mode:
            print(statement,values)
        return