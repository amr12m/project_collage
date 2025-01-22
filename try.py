import os
import time
import datetime
import re

def run_commend(commend):
    com = os.system(commend)
    return com


def subzy_fun():
    com = f'python fuzzer.py "ffuf -w ./fuzz.txt -u http://example.com/FUZZ"'
    output = run_commend(com)

subzy_fun()