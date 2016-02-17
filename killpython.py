#!/usr/bin/env python3.4
"""
kill_python.py,
copyright (c) 2015 by Stefan Lehmann

"""
import os
import psutil

PROC = "python.exe"
my_pid = os.getpid()

i = 0
for p in psutil.process_iter():
    if p.name() == PROC and p.pid != my_pid:
        i += 1
        p.kill()

print("Killed {} instances of process '{}'.".format(i, PROC))
