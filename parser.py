#!/usr/bin/env python3
from lark import Lark, v_args, Transformer, Tree
math_grammar = """     
    ?start: sum
    ?sum: product
        | sum "+" product    -> add
        | sum "-" product    -> sub
    ?product: atom
        | product "*" atom   -> mul
        | product "/" atom   -> div
    ?atom: NUMBER -> number
        | atom "**" atom     -> pow
        | "-" atom           -> neg
        | "(" sum ")"
        | var
        | function           -> func
    ?function: 
        | "sin" "(" sum ")"  -> sin
        | "asin" "(" sum ")" -> asin
        | "cos" "(" sum ")"  -> cos
        | "acos" "(" sum ")" -> acos
        | "tan" "(" sum ")"  -> tan
        | "atan" "(" sum ")" -> atan
        | "exp" "(" sum ")"  -> exp
        | "sqrt" "(" sum ")" -> sqrt
        | "ln" "(" sum ")"   -> ln
        | "tan" "(" sum ")"  -> tan
    var : "x" -> x 
        | "y" -> y 
        | "z" -> z



    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg, pow
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        return self.vars[name]
#for test calculation ONLY with numbers




calc_parser = Lark(math_grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse
tree_parser = Lark(math_grammar, parser = 'lalr')
parse = tree_parser.parse

if __name__ == "__main__":
    mathexpr = "-cos(y+3*7)**(sin(y)+3)+2**cos(z-y**2)"
    print(mathexpr, "tree:")
    print(parse(mathexpr).pretty())


