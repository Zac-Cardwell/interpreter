

import lexical_analyzer
import extra

line = lexical_analyzer.lexical()


Arithmetic_op = ['Arithmetic_op', 'add_operator', 'sub_operator',
                 'mul_operator', 'div_operator']
Arithmetic_expression = ['assignment_operator',
                         'id', 'literal_integer', 'arithmetic_op']
Relative_op = ['Relative_op', 'le_operator', 'lt_operator', 'ge_operator',
               'gt_operator', 'eq_operator', 'ne_operator']
Print_statement = ['Print_statement', 'print']
identifiers = ['if', 'while', 'print', 'id']


def randoms(input):
    fun = []
    i = 0
    if input[i].func == 'function':
        fun.append(input[i])
        i += 1
        if input[i].func == 'function_ID':
            fun.append(input[i])
            i += 1
            if parsblock(input, i) != None:
                temp, i = parsblock(input, i)
                fun.append(temp)
                if input[i].func == 'end':
                    return fun
                elif type(parsblock(input, i)) != "error":
                    temp, i = parsblock(input, i)
                    fun.append(temp)
                    if input[i].func == 'end':
                        return fun
                else:
                    print('Fail')

            else:
                print('error 2', parsblock(input, i))
    return "Error randoms"

# most broad class in parser can either be a statment or a statment followed by another block
# passes on input until end keyword is reached and program return final form
# takes the output of other functions and puts them in an array


def parsblock(input, pos):
    block = []
    while pos < len(input):
        if input[pos].func == 'end':
            block.append(input[pos])
            return block, pos
        elif input[pos].func == 'else':
            return block, pos-1
        elif type(pars_statement(input, pos)) != "Error pars_statment":
            temp, pos = pars_statement(input, pos)
            block.append(temp)
            if pos + 1 >= len(input):
                return block, pos
            pos += 1
        else:
            print("block_fail")
            return pars_statement(input[pos], pos), pos
    print('failzzzzzzzzzzzz')

# determines if input is a statment
# each statment starts with its own keyword (if, while, id, print)
# input is passed to correct function for evaluation
# if keyword is not associated with a function returns error


def pars_statement(input, pos):
    if input[pos].func == 'while':
        return while_pars(input, pos)
    elif input[pos].func == 'if':
        return parsif(input, pos)
    elif input[pos].func == 'id':
        return assignpars(input, pos)
    elif input[pos].func == 'print':
# here
        return input[pos], pos
    else:
        print("pars_error", input[pos])
        return "Error pars_statment", pos


# determines if input contains an if statment
# input will be evaluated word by word until End keyword is found
# sub statments will be passed on to their respective functions
# if order and sytax of input doesnt match function error is thrown
# returns a class with data orgonized into if, then, else catagories


def parsif(input, pos):
    if_state = []
    if_state.append(input[pos])
    if type(bool_exp(input, pos+1)) != "<class 'str'>":
        temp, pos = bool_exp(input, pos+1)
        ifx = extra.ifz(temp, pos)
        if_state.append(temp)
        pos += 1
        if input[pos].func == 'then':
            if_state.append(input[pos])
            pos += 1
            if type(parsblock(input, pos)) != "<class 'str'>":
                temp, pos = parsblock(input, pos)
                ifx.add_then(temp, pos)
                if_state.append(input[pos])
                pos += 1
                if input[pos].func == 'else':
                    if_state.append(input[pos])
                    pos += 1
                    if type(pars_statement(input, pos)) != "<class 'str'>":
                        temp, pos = pars_statement(input, pos)
                        ifx.add_else(temp, pos)
                        if_state.append(input[pos])
                        pos += 1
                        if input[pos].func == 'end':
                            if_state= [ifx, input[pos]]
# here
                            return if_state , pos
    print("Error if statment")
    return "Error if statment", pos


# determines if input contains a while statment
# input will be evaluated word by word until End keyword is found
# sub statments will be passed on to their respective functions
# if order and sytax of input doesnt match while function syntax error is thrown
# returns class with data for bool exp and the do func


def while_pars(input, pos):
    while_state = []
    while_state.append(input[pos])
    if type(bool_exp(input, pos+1)) != "<class 'str'>":
        temp, pos = bool_exp(input, pos+1)
        whl = extra.whilez(temp, pos)
        while_state.append(temp)
        pos += 1
        if input[pos].func == 'do':
            while_state.append(input[pos])
            pos += 1
            if type(parsblock(input, pos)) != "<class 'str'>":
                temp, pos = parsblock(input, pos)
                whl.add_do(temp, pos)
                while_state.append(temp)
                if input[pos].func == 'end':
                    while_state.append(input[pos])
                    while_state = [whl, input[pos]]
# here
                    return while_state, pos
    print("Error While statment")
    return "Error While statment", pos




# sub functions


# determines if input is an assignment function
# if assign function cantains an arithmic exp sub functions are called
# returns class containing data


def assignpars(input, pos):
    assignment = []
    if input[pos].func == 'id':
        assignment.append(input[pos])
        pos += 1
        if input[pos].func == 'assignment_operator':
            assignment.append(input[pos])
            pos += 1
            if check(input[pos]) == 'Arithmetic_expression':
                if check(input[pos+1]) == 'Arithmetic_op':
                    temp, pos = arith_exp(input, pos)
                    if temp != "arith_exp Error":
                        assignment.append(temp)
                        ass = extra.assign_expz(assignment, pos)
                        return ass, pos
                else:
                    assignment.append(input[pos])
                    ass = extra.assign_expz(assignment, pos)
                    return ass, pos
    print("Error assign statment")
    return "Error assign statment", pos


# determines if input is a boolean expression
# if bool function cantains an arithmic exp sub functions are called
# returns class containing data


def bool_exp(input, pos):
    bool = []
    if check(input[pos]) == 'Relative_op':
        bool.append(input[pos])
        pos += 1
        if check(input[pos]) == 'Arithmetic_expression':
            bool.append(input[pos])
            pos += 1
            if check(input[pos]) == 'Arithmetic_expression':
                bool.append(input[pos])
# here
                bool_ = extra.bool_expz(bool, pos)
                return bool_, pos
    print("Error Bool statment")
    return "Error Bool statment", pos


# determines if input is a boolean expression
# returns values in a custom class

def arith_exp(input, pos):
    exp = []
    if check(input[pos]) == 'Arithmetic_expression':
        if check(input[pos+1]) == 'Arithmetic_op':
            if check(input[pos+2]) == 'Arithmetic_expression':

                if check(input[pos+3]) == 'Arithmetic_op':
                    temp, posz = arith_exp(input, pos+2)
                    if temp != "arith_exp Error":
                        exp = [input[pos], input[pos + 1]] + temp.data
                        ar = extra.arith_expz(exp, pos)
                        return ar, posz
                else:
                    exp = [input[pos], input[pos + 1], input[pos + 2]]
                    ar = extra.arith_expz(exp, pos+2)
                    return ar, pos+2
    print("arith_exp Error")
    return "arith_exp Error", pos




# checks if the input is in one of the given lists
def check(i):
    for j in Arithmetic_op:
        if i.func == j:
            return 'Arithmetic_op'
    for j in Arithmetic_expression:
        if i.func == j:
            return 'Arithmetic_expression'
    for j in Relative_op:
        if i.func == j:
            return 'Relative_op'
    for j in Print_statement:
        if i.func == j:
            return 'Print_statement'
    return 'false'






# extra shit i need to fix
function = []
mainz = []
for i in line:
    if i != 'Error':
        for j in i:
            if j != 'Error':
                    mainz.append(j)

tep = []
tepz = []
function1 = []
main = []
what = True
for i in range(0, len(mainz)-1):
    if mainz[i+1].func == 'function' and what is False:
        tepz.append(mainz[i])
        main.append(list(tepz))
        tepz.clear()
    else:
        what = False
        tepz.append(mainz[i])

main.append(list(tepz))
def get_das():
    return main


