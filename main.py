from Logic.grammar import Grammar
from pprint import pprint

def menu():
    while True:
        selection = input("\nStart Top Down Parsing? [y/Y]: ")
        if  selection != 'y': break
        if selection != 'Y': break
    
    G = Grammar()

    while True:
        print("\n######################################")
        print("\nMENU")
        print("\t[1] See First and Follow")
        print("\t[2] See Parsing Table")
        print("\t[3] See Derivation Tree")
        print("\t[0] Exit")
        selection = input("\nWhat do you want to do?: ")
        print("\n######################################")
        
        if  selection == '1':
            print("\nFirst:\n", G.first)
            print("\nFollow:\n", G.follow)

        elif selection == '2':
            print("\nParsing Table:\n")
            pprint(G.parsing_table)

        elif  selection == '3':
            print("\nTree:\n", G.tree)

        else: break
    
    print("\nBye!\n")

    

if __name__ == '__main__':
    x = ''
    while True:
        x = input('\nHave you already specified the grammar to input in the \"Grammar_Input.txt\" file? [y/Y]: ')
        if  x != 'y': break
        if x != 'Y': break
    menu()