from sys import argv
from onlineUtilityFunctions import evaluateSentance

# Run this file for command line functionality
# Can pass a file to return beats per line, or can pass a sentance for evaluating that sentance
argv.pop(0)
inputString = argv

if inputString[0].endswith(".txt"):
    print("****************************************************")
    with open(inputString[0]) as file:
        for line in file:
            print(line)
            evaluateSentance(line.split())
            print("-----------------------------------------------------")
    print("****************************************************")
else:
    print("****************************************************")
    print(inputString)
    evaluateSentance(inputString)
    print("****************************************************")



# TODO add way of using offline downloaded dictionary to get stresses (may need new module)
