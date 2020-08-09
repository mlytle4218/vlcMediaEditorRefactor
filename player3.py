#!/usr/bin/env python3
# import curses
from curses import wrapper
import sys

#local imports
from main import start
from main import state
from main import help



if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            help.printHelp()
        else:
            command = []
            # state = State()
            
            wrapper(start.start, [command, sys.argv[1]])
            print(len(command))
            print(command)
    else:
        print("requires a file to edit")