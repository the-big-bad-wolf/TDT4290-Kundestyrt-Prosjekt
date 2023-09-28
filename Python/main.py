import argparse

from crunch import start_processes

if __name__ == '__main__':
    # start program
    start_processes(False)

"""
Use this to move csv to different folder on exit
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

import sys
signal.signal(signal.SIGINT, signal_handler)
"""
