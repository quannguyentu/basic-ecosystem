#this program runs from Linux terminal using the following syntax:
#python main.py inputfile
#inputfile is the filename of the initial configuration of the ecosystem
# Ramon Asuncion and Quan Nguyen
# Monday, September 13, 11:00 PM
# CSCI 204 - Dancy
# Project 1, Phase 2
from Ecosystem_QUAN import Ecosystem
from River import River

import sys
def main():
    if len( sys.argv ) != 2:
        inputfile = input("Name of input file: ")
    else:    
        # Pick up the command line argument   
        inputfile = sys.argv[1]
    print(inputfile)

    ecosystem = Ecosystem(inputfile)
    river = River(ecosystem, 3)
    river.run()

main()
