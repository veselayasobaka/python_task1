#!/usr/bin/env python3
from lark import Lark, v_args, Transformer, Tree
from lark.lexer import Token
from lark.visitors import Interpreter
math_grammar = """     
    ?start: sum
    ?sum: product
        | sum "+" product    -> add
        | sum "-" product    -> sub
    ?product: atom
        | product "*" atom   -> mul
        | product "/" atom   -> div
    ?atom: NUMBER -> number
        | atom "^" atom     -> pow
        | "-" atom           -> neg
        | "(" sum ")"
        | var
        | function           
    function: 
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
    !var : "x" 
        | "y"
        | "z"


    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

   
class SimplifyTree(Transformer):

    def add(self, tree):
        (left, right) = tree
        if left.data == right.data == 'number':
            summ = float(''.join(left.children))+float(''.join(right.children))
            return Tree('number', [Token('NUMBER', str(summ))])
        elif left.data == 'number' and float(''.join(left.children)) == 0:
            return right
        elif right.data == 'number' and float(''.join(right.children)) == 0:
           return left
        else: return Tree('add', tree)

    def sub(self, tree):
        (left, right) = tree
        if left.data == right.data == 'number':
            summ = float(''.join(left.children))-float(''.join(right.children))
            return Tree('number', [Token('NUMBER', str(summ))])
        elif left.data == 'number' and float(''.join(left.children)) == 0:
            return Tree('neg', [right])
        elif right.data == 'number' and float(''.join(right.children)) == 0:
           return left
        else: return Tree('sub', tree)

    def mul(self, tree):
        (left, right) = tree
        if left.data == right.data == 'number':
            summ = float(''.join(left.children))*float(''.join(right.children))
            return Tree('number', [Token('NUMBER', str(summ))])
        elif left.data == 'number' and float(''.join(left.children)) == 0:
            return Tree('number', [Token('NUMBER', '0')])
        elif right.data == 'number' and float(''.join(right.children)) == 0:
            return Tree('number', [Token('NUMBER', '0')])
        else: return Tree('mul', tree)

    def div(self, tree):
        (left, right) = tree
        if left.data == right.data == 'number':
            summ = float(''.join(left.children))/float(''.join(right.children))
            return Tree('number', [Token('NUMBER', str(summ))])
        elif left.data == 'number' and float(''.join(left.children)) == 0:
            return Tree('number', [Token('NUMBER', '0')])
        else: return Tree('div', tree)

    def pow(self, tree):
        (left, right) = tree
        if left.data == right.data == 'number':
            summ = float(''.join(left.children))^float(''.join(right.children))
            return Tree('number', [Token('NUMBER', str(summ))])
        elif left.data == 'number' and float(''.join(left.children)) == 0:
            return Tree('number', [Token('NUMBER', '0')])
        elif right.data == 'number' and float(''.join(right.children)) == 0:
            return Tree('number', [Token('NUMBER', '1')])
        elif left.data == 'number' and float(''.join(left.children)) == 1:
            return Tree('number', [Token('NUMBER', '1')])
        elif right.data == 'number' and float(''.join(right.children)) == 1:
            return left
        else: return Tree('pow', tree)
    
    def neg(self, tree):
        (child,) = tree
        if child.data == 'number':
            numb = float(''.join(child.children))
            return Tree('number', [Token('NUMBER', str(-numb))])
        else: return Tree('neg', tree)

class DiffTree(Interpreter):

    def var(self, tree):
        varbl = ''.join(tree.children)
        if varbl == 'x':
            return Tree('number', [Token('NUMBER', '1')])
        else:
            return Tree('number', [Token('NUMBER', '0')])

    def number(self, tree):
        return Tree('number', [Token('NUMBER', '0')])

    def add(self, tree):
        return Tree('add', self.visit_children(tree))

    def sub(self, tree):
        return Tree('sub', self.visit_children(tree))

    def mul(self, tree):
        (left, right) = tree.children
        return Tree('add', [
            Tree('mul', [self.visit(left), right]),
            Tree('mul', [left, self.visit(right)])])

    def div(self, tree):
        (left, right) = tree.children
        return Tree('div', [
            Tree('sub', [
                Tree('mul', [self.visit(left), right]),
                Tree('mul', [left, self.visit(right)])]), 
            Tree('mul', [right, right])])

    def neg(self, tree):
        (child,) = tree.children
        return Tree('neg', [self.visit(child)])

    def pow(self, tree):
        (left, right) = tree.children
        if right.data == 'number':
            coeff = float(''.join(right.children))
            return Tree('mul', [
                Tree('mul', [
                    Tree('number', [Token('NUMBER', coeff)]),
                    Tree('pow', [
                         left, 
                         Tree('number', [Token('NUMBER', coeff-1)])])]),
                self.visit(left)])
        else:
            return self.visit(Tree('exp', [Tree('mul', [Tree('ln', [left]), right])]))
        
    def sin(self, tree):
        (child,) = tree.children
        return Tree('mul', [Tree('cos', [child]), self.visit(child)])

    def asin(self, tree):
        (child,) = tree.children
        return Tree('mul', [
            Tree('div', [
                Tree('number', [Token('NUMBER', '1')]), 
                Tree('sqrt', [
                    Tree('sub', [
                        Tree('number', [Token('NUMBER', '1')]), 
                        Tree('pow', [
                            child, 
                            Tree('number', [Token('NUMBER', '2')])])])])]),

            self.visit(child)])

    def cos(self, tree):
        (child,) = tree.children
        return Tree('neg', [
            Tree('mul', [Tree('sin', [child]), self.visit(child)])])

    def acos(self, tree):
        (child,) = tree.children
        return Tree('mul', [
            Tree('div', [
                Tree('number', [Token('NUMBER', '-1')]), 
                Tree('sqrt', [
                    Tree('sub', [
                        Tree('number', [Token('NUMBER', '1')]), 
                        Tree('pow', [
                            child, 
                            Tree('number', [Token('NUMBER', '2')])])])])]),

            self.visit(child)])

    def tan(self, tree):
        (child,) = tree.children
        return Tree('mul', [
            Tree('pow', [
                Tree('cos', [child]), 
                Tree('number', [Token('NUMBER', '-2')])]), 
            self.visit(child)])

    def atan(self, tree):
        (child,) = tree.children
        return Tree('mul', [
            Tree('div', [
                Tree('number', [Token('NUMBER', '1')]), 
                Tree('add', [
                    Tree('number', [Token('NUMBER', '1')]), 
                    Tree('pow', [
                        child, 
                        Tree('number', [Token('NUMBER', '2')])])])]),
            self.visit(child)])

    def exp(self, tree):
        (child,) = tree.children
        return Tree('mul', [Tree('exp', [child]), self.visit(child)])

    def ln(self, tree):
        (child,) = tree.children
        return Tree('mul', [
            Tree('div', [Tree('number', [Token('NUMBER', '1')]), child]), 
            self.visit(child)])

    def sqrt(self, tree):
        (child,) = tree.children
        return Tree('mul', [
            Tree('div', [
                Tree('number', [Token('NUMBER', '1')]), 
                Tree('mul', [
                    Tree('number', [Token('NUMBER', '2')]), 
                    Tree('sqrt', [child])])]), 
            self.visit(child)])

class TreeToString(Transformer):
    def add(self, vals):
        valslist = "("+ vals[0]+ '+'+ vals[1]+ ")" 
        return  valslist
    def sub(self, vals):
        valslist = "("+ vals[0]+ '-'+ vals[1]+ ")" 
        return  valslist
    def mul(self, vals):
        valslist = "("+ vals[0]+ '*'+ vals[1]+ ")" 
        return  valslist
    def div(self, vals):
        valslist = "("+ vals[0]+ '/'+ vals[1]+ ")" 
        return  valslist
    def pow(self, vals):
        valslist = "("+ vals[0]+ '^'+ vals[1]+ ")" 
        return  valslist
    def neg(self, vals):
        valslist = "("+ "-"+ vals[0]+ ")"
        return valslist
    def number(self, s):
        return ''.join(s)
    def sin(self, vals):
        if vals[0][0] == '(':
            funclist = "sin"+ ''.join(vals)
            return funclist
        else:
            funclist = "sin("+ ''.join(vals)+ ")"
            return funclist
    def cos(self, vals):
        if vals[0][0] == '(':
            funclist = "cos"+ ''.join(vals)
            return funclist
        else:
            funclist = "cos("+ ''.join(vals)+ ")"
            return funclist
    def tan(self, vals):
        if vals[0][0] == '(':
            funclist = "tan"+ ''.join(vals)
            return funclist
        else:
            funclist = "tan("+ ''.join(vals)+ ")"
            return funclist
    def asin(self, vals):
        if vals[0][0] == '(':
            funclist = "asin"+ ''.join(vals)
            return funclist
        else:
            funclist = "asin("+ ''.join(vals)+ ")"
            return funclist
    def acos(self, vals):
        if vals[0][0] == '(':
            funclist = "acos"+ ''.join(vals)
            return funclist
        else:
            funclist = "acos("+ ''.join(vals)+ ")"
            return funclist
    def atan(self, vals):
        if vals[0][0] == '(':
            funclist = "atan"+ ''.join(vals)
            return funclist
        else:
            funclist = "atan("+ ''.join(vals)+ ")"
            return funclist
    def exp(self, vals):
        if vals[0][0] == '(':
            funclist = "exp"+ ''.join(vals)
            return funclist
        else:
            funclist = "exp("+ ''.join(vals)+ ")"
            return funclist
    def sqrt(self, vals):
        if vals[0][0] == '(':
            funclist = "sqrt"+ ''.join(vals)
            return funclist
        else:
            funclist = "sqrt("+ ''.join(vals)+ ")"
            return funclist
    def ln(self, vals):
        if vals[0][0] == '(':
            funclist = "ln"+ ''.join(vals)
            return funclist
        else:
            funclist = "ln("+ ''.join(vals)+ ")"
            return funclist
    def var(self, vals):
        return ''.join(vals)


tree_parser = Lark(math_grammar, parser = 'lalr')
parse = tree_parser.parse

def derive(func):
    tree_parser = Lark(math_grammar, parser = 'lalr')
    parse = tree_parser.parse
    tree = parse(func)
    visitor = DiffTree()
    diff_tree = visitor.visit(tree)
    s = SimplifyTree().transform(diff_tree)
    return TreeToString().transform(s)

if __name__ == "__main__":
    mathexpr = "(sin(x^1))^1"
    print(mathexpr, "\ttree:\n")
    tree = parse(mathexpr)
    print(tree)
    print(tree.pretty())
    s = SimplifyTree().transform(tree)
    print(s)
    print(s.pretty())
'''
    visitor = DiffTree()
    diff_tree = visitor.visit(tree)
    print(diff_tree)
    print(diff_tree.pretty())
    s = SimplifyTree().transform(diff_tree)
    print(s)
    print(s.pretty())
    d = TreeToString().transform(s)
    print(d)
'''



