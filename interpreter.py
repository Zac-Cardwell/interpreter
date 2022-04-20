from Parser import *
from extra import *

global_var = []

main = get_das()
tep1 = randoms(main[0])
tep2 = randoms(main[1])
tep3 = randoms(main[2])

def runz(input):
    for i in range(len(input)):
        if isinstance(input[i], list):
            runz(input[i])
        else:
            find_fuc(input[i], global_var)
runz(tep2)