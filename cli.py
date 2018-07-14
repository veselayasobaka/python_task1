#!/usr/bin/env python3
from differentiator import derive
print("The program differentiates the entered mathematical " 
      "expression in the x variable and supports the use of " 
      "variables x, y, z, operators '+', '-', '*', '/', '^' '(', ')'" 
      "and functions sin(), cos(), tan(), asin(), acos(), "
      "atan(), ln(), exp(), sqrt()")
print("Input mathematical expression:")
while(True):
    try:
        mathexpr = input()
        if mathexpr == "":break
        answer = derive(mathexpr)
    except ZeroDivisionError:
        print("Error! Zero division detected.")
    except Exception as err:
        print(str(err)+"Unkown error. Check the input line.")
    else:
        print(answer)


