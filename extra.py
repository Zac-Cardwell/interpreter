
# class for the bool functions
# has function (get_answer) to solve for the bool expression and returns true or false

class bool_expz:
    def __init__(self, data, pos):
        self.data = data
        self.end_pos = pos


    def get_answer(self, global_var):
        alt = list(self.data)
        for i in range(len(alt)):
            if alt[i].data == '~=':
                alt[i].data = '!='
            for j in global_var:
                if alt[i].data == j.var:
                    alt[i] = j.data
        temp = ' '
        try:
            temp += str(alt[1].data) + ' '
        except:
            temp += str(alt[1]) + ' '
        try:
            temp += str(alt[0].data) + ' '
        except:
            temp += str(alt[0]) + ' '
        try:
            temp += str(alt[2].data) + ' '
        except:
            temp += str(alt[2]) + ' '
        return(eval(temp))


# class for arith expressions
# has function to solve for the given expression
class arith_expz:
    def __init__(self, data, pos):
        self.data = data
        self.end_pos = pos
        self.type = 'arith'

    def solve_data(self, global_var):
        temp = list(self.data)
        for x in range(len(self.data)):
            if type(self.data[x].data) is str:
                for i in global_var:
                    if i.var == self.data[x].data:
                        temp[x] = str(i.data)
        tempz = []
        for a in range(len(self.data)):
            try:
                tempz.append(temp[a].data)
            except:
                tempz.append(temp[a])
        outz = " "
        for i in tempz:
            outz += " "+i
        temp.clear()
        return (eval(outz))



# custom class for assignment expressions
# first function returns the left and right side of the function for later use
# second functions finds all variables and assigns them a value
# third function solves a given assignment expression
class assign_expz:
    def __init__(self, data, pos):
        self.data = data
        self.end_pos = pos
        self.type = 'assign'

    def get_data(self, global_var):
        left_data = []
        right_data = []
        temp = self.data
        for p in range(len(temp)):
            try:
                if self.data[p].func == 'assignment_operator':
                    i = p
            except:
                continue
        for j in range(0, len(self.data)):
            if j < i:
                left_data.append(self.data[j])
            if j > i:
                right_data.append(self.data[j])
        check_var(left_data, right_data, global_var)
        return left_data, right_data

    def check_data(self, global_var):
        left, right = self.get_data(global_var)
        check_var(left, right, global_var)

    def slove(self, global_var):
        left, right = self.get_data(global_var)
        try:
            for i in range(0, len(global_var)):
                if global_var[i].var == left[0].data:
                    if right[0].type == 'arith':
                        global_var[i].reassign_var(right[0].solve_data(global_var))
                    else:
                        global_var[i].reassign_var(right[0].data)
        except:
            print('errorz')
            return



# custom class for while expressions
# contains data for the bool expression and for the do expression so the can be evaluated
# solve function completes the while function
class whilez:
    def __init__(self, data, pos):
        self.while_data = data
        self.while_pos = pos
        self.type = 'whilez'

    def add_do(self, data, pos):
        self.do_data = data
        self.do_pos = pos

    def solve(self, global_var):
        while self.while_data.get_answer(global_var) == True:
            for i in self.do_data:
                if i.data == 'end':
                    break
                elif i.data == 'print':
                    print('fix this')
                else:
                    try:
                        i.check_data(global_var)
                        if find_fuc(i, global_var) is False:
                            print('Error')
                    except:
                        print('error')
                        break



# custom class for if statment
# contains main bool function and then/else functions
# Solve function executes the if statment and calls proper sub statment (then/else)
class ifz:
    def __init__(self, data, pos):
        self.ifs_pos = pos
        self.if_data = data
        self.type = 'ifz'

    def add_then(self, data, then_pos):
        self.then_fuc = data
        self.then_pos = then_pos

    def add_else(self, data, then_pos):
        self.else_fuc = data
        self.else_pos = then_pos

    def solve(self, global_var):
        if self.if_data.get_answer(global_var) == True:
            for i in self.then_fuc:
                if i.data == 'end':
                    break
                elif i.data == 'print':
                    printz(i, global_var)
                else:
                    try:
                        i.check_data(global_var)
                        if find_fuc(i, global_var) is False:
                            print('Error')
                    except:
                        print('error')
                        break
        else:
            try:
                i = self.else_fuc
                if i.data == 'end':
                    return
                elif i.data == 'print':
                    printz(i, global_var)
                else:
                    try:
                        i.check_data(global_var)
                        if find_fuc(i, global_var) is False:
                            print('Error')
                    except:
                        print('error')
            except:
                return


# executes the print statment
def printz(input, global_var):
    line = list(input.paren)
    for p in range(len(line)):
        for h in global_var:
            if line[p] == h.var:
                line[p] = h.data
    outz = ''
    for x in line:
        outz += str(x) + ' '
    print(eval(outz))



# class to hold all the variables of the program
class varz:
    def __init__(self, var, data):
        self.var = var
        self.data = data

    def reassign_var(self, input):
        self.data = input


# checks to see if a variable exists and creats one if it doesnt
def check_var(left, right, global_var):
    new = False
    if len(global_var) == 0:
            if type(right[0].data) == str:
                temp = varz(left[0].data, right[0].data)
                global_var.append(temp)
            else:
                temp = varz(left[0].data, right[0].solve_data(global_var))
                global_var.append(temp)

    else:
        for i in global_var:
            if i.var == left[0].data:
                if type(right[0].data) == str:
                 continue
            else:
                new = True

        if new is True:
            try:
                if type(right.data) == int:
                    temp = varz(left.data, right.data)
                    global_var.append(temp)
            except:
                temp = varz(left.data, right.solve_data(global_var))
                global_var.append(temp)



# calls the right function depending on the input
def find_fuc(input, global_var):
    if input.type == 'arith':
        input.solve_data(global_var)
    elif input.type == 'assign':
        input.slove(global_var)
    elif input.type == 'whilez':
        input.solve(global_var)
    elif input.type == 'ifz':
        input.solve(global_var)
    elif input.type == 'token':
        try:
            if input.func != 'function_ID':
                printz(input, global_var)
        except:
            return
    else:
        print("Error find_fuc")