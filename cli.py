#!/usr/bin/env python3
from differentiator import derive
print("Input mathematical expression:")
while(True):
    try:
        mathexpr = input()
        if mathexpr == "": break
        answer = derive(mathexpr)
    except ZeroDivisionError:
        print("Error! Zero division detected.")
    except Exception as err:
        print(str(err)+"Unkown error. Check the input line.")
    else:
        print(answer)


