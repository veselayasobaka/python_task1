#!/usr/bin/env python3
from parser import derive

funcs = ['exp(x)', 
         'x-y', 
         'x+2']

for func in funcs:
    print(func + ': '+ '\n' + derive(func) + '\n')
