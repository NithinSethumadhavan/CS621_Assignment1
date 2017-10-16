# Submitted by Abhijeet Dubey and Nithin S  for CS 621: Artificial Intelligence Assignment 1 (October 2017)
#

import sys

"""
Python script to read rules from a file rules.txt and convert them into python objects.
"""


class Rule:
    """
    Represents a rule which has a term on left and right hand sides.
    """
    lhs = None
    rhs = None

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " -> " + str(self.rhs)


class Term:
    """
    Represents a term, specifically this class represents terms which take any number of arguments.
    """
    sym = None
    next = None
    args = None
    kwargs = None

    def __init__(self, *args, **kwargs):
        self.sym = kwargs['sym'] if 'sym' in kwargs else None
        self.rhs = kwargs['next'] if 'rhs' in kwargs else None
        self.args = list(args)

    def __str__(self):
        ret = self.sym + "("
        for t in self.args:
            ret += str(t) + ","
        ret = ret[:-1]
        ret += ")"
        return ret

    def describe(self, prefix=""):
        print_line(prefix, 20)
        print(prefix + "Type: term")
        print(prefix + "Term: " + str(self))
        print(prefix + "Arity: " + str(len(self.args)))
        print(prefix + "Symbol: " + str(self.sym))
        if len(self.args) > 0:
            print(prefix + "Arguments:")
            i = 1
            for arg in self.args:
                print(prefix + str(i) + ":")
                i += 1
                arg.describe(prefix=prefix + "\t | ")
        print_line(prefix, 20)


class Variable(Term):
    """
    Represents a variable, which is sort of a term, hence the inheritance
    """
    name = None
    value = None

    def __init__(self, name):
        Term.__init__(self)
        self.name = name

    def __str__(self):
        return str(self.name)

    def describe(self, prefix=""):
        print_line(prefix, 20)
        print(prefix + "Type: variable")
        print(prefix + "Name: " + str(self))
        print_line(prefix, 20)


class Constant(Term):
    """
    Represents a constant, which is sort of a term, hence the inheritance
    """
    value = None

    def __init__(self, value):
        Term.__init__(self)
        self.value = value

    def __str__(self):
        return str(self.value)

    def describe(self, prefix=""):
        print_line(prefix, 20)
        print(prefix + "Type: constant")
        print(prefix + "Value: " + str(self))
        print_line(prefix, 20)


def print_line(prefix, n):
    li = prefix.rsplit('\|\s$', 1)
    li = ''.join(li)
    print(li + "-" * n)


def parse_term(term):
    stack = []
    symbols = ['+', '*', 's', 'E', 'fact']
    variables = ['u', 'v', 'w', 'x', 'y', 'z']
    constants = ['0', 'T', 'F']
    for c in term:
        if c in symbols:
            stack.append(c)
        if c == '(':
            stack.append(c)
        if c in variables:
            stack.append(Variable(c))
        if c in constants:
            stack.append(Constant(c))
        if c == ')':
            t = stack.pop(-1)
            args = []
            while t != '(':
                args.append(t)
                t = stack.pop(-1)
            t = stack.pop(-1)
            args = tuple(args[::-1])
            stack.append(Term(*args, sym=t))
    return stack.pop(-1)


def convert_rules(rules):
    conv_rules = []
    for rule in rules:
        if rule.strip():
            lhs = rule.split("->")[0].strip()
            rhs = rule.split("->")[1].strip()
            lhs = parse_term(lhs)
            rhs = parse_term(rhs)
            lhs.next = rhs
            conv_rules.append(Rule(lhs, rhs))

    return conv_rules


def print_rules(rules):
    for rule in rules:
        print("-" * 50)
        print("Rule: " + str(rule))
        print()
        print("LHS:")
        rule.lhs.describe(prefix="\t | ")
        print()
        print("RHS:")
        rule.rhs.describe(prefix="\t | ")
        print("-" * 50)
        print()


def main():
    # filename = sys.argv[1]
    filename = "rules.txt"
    rule_file = open(filename, 'r')
    rules_txt = rule_file.read().split('\n')
    rules = convert_rules(rules_txt)
    print_rules(rules)

    # term = input("The term to evaluate: ")
    term = "+(s(s(0)),s(s(0)))"
    term = parse_term(term)
    term.describe(prefix="| ")


if __name__ == "__main__":
    main()
