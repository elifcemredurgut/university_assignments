import sys
import FindCitations
import FindCyclicReferences

typ = sys.argv[0]
num = int(sys.argv[1])
file_name = sys.argv[2]

if typ == "COUNT":
    instance = FindCitations(num)
    instance.start(file_name)
elif typ == "CYCLE":
    instance = FindCyclicReferences(num)
    instance.start(file_name)
else:
    print("You have antered an invalid operation type!")


