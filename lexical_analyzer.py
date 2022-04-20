

import re


class token:
    def __init__(self, func, data):
        self.data = data
        self.func = func
        self.type = 'token'

    def set_paren(self, data):
        self.paren = data



def extract(string, start='(', stop=')'):
    return string[string.index(start) + 1:string.index(stop)]

# creates the tokens for operator and keyword functions
op1 = token('assignment_operator', '=')
op2 = token('le_operator', '<=')
op3 = token('lt_operator', '<')
op4 = token('ge_operator', '>=')
op5 = token('gt_operator', '>')
op6 = token('eq_operator', '==')
op7 = token('ne_operator', '~=')
op8 = token('add_operator', '+')
op9 = token('sub_operator', '-')
op10 = token('mul_operator', '*')
op11 = token('div_operator', '/')
op12 = token('note', '//')
op13 = token('pl_eq_operator', '+=')
operator = [op1, op2, op3, op4, op5, op6,
            op7, op8, op9, op10, op11, op12, op13]
functions = ["function", "print", "while", "if", "else", "end", "do", "then"]


def scanner(input):
    line = []
    for x in input:
        if x.isdigit():
            temp = token('literal_integer', x)
            line.append(temp)
        elif (x.find('//') != -1):
            return 'note'
        else:
            maybe = False
            for j in operator:
                if x == j.data:
                    if x == op12.data:
                        temp = token(j.fun, input)
                        line.append(temp)
                        return line
                    temp = token(j.func, x)
                    line.append(temp)
                    maybe = True
                    ###################
            for j in functions:
                if x.find(j) == 0 or x == j:
                    temp = token(j, j)
                    if (x.find('(') != -1) and (x.find(')') != -1):
                        res = re.findall(r'\(.*?\)', x)
                        temp.set_paren(extract(res[0]))
                    line.append(temp)
                    maybe = True
            if maybe is False and len(x) == 1:
                temp = token('id', x)
                line.append(temp)
            elif maybe is False:
                if (x.find('(') != -1) and (x.find(')') != -1):
                    if x.find('(') != 0:
                        ind = x.find('(')
                        a, b = x[:ind], x[ind:]
                        temp = token('function_ID', a)
                        temp.set_paren(b)
                        line.append(temp)
                    else:
                        res = re.findall(r'\(.*?\)', x)
                        temp = token('parenthesis', x)
                        temp.set_paren(res)
                        line.append(temp)
                else:
                    return "Error"
    return line


def lexical():
    # you must change the address to make this work on a diffrent computer
    f = open("C://Users//zacca//Documents//Python Projects//Interpreter//test.txt")
    abc = []
    for x in f:
        if x.strip() == '':
            continue
        y = x.split()
        line = scanner(y)
        if line != "note":
            abc.append(line)
    return abc


leng = 0


def next_line():
    global leng
    tester = lexical()
    if leng < len(tester):
        temp = tester[leng]
        leng = leng + 1
        return temp
    elif leng >= len(tester):
        leng = 0
        return "Done"


def lexical3():
    # you must change the address to make this work on a diffrent computer
    f = open("C://Users//zacca//Documents//Python Projects//Interpreter//test.txt")
    print("___table___")
    for x in f:
        if x.strip() == '':
            continue
        y = x.split()
        line = scanner(y)
        if line == "Error":
            print(line)
        elif line[0] == "note":
            continue
        else:
            # work in ask operator for returning line
            for j in line:
                print(j.func, end=" ")
                print("\t", j.data)
                if j.paren is not None:
                    print(j.paren)

