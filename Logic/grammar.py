from Logic.node import Node

class Grammar():
    
    def __init__(self):
        self.G = self.input_grammar()
        self.keys = self.get_keys()
        self.sub_keys = self.get_sub_keys()
        self.terminals = self.get_terminals()
        self.first = self.First()
        self.follow = self.Follow()
        self.parsing_table = self.Parsing_table()
        self.stack = ['$', 'S']
        self.w = self.input_w()
        self.root = Node(self.stack[-1], None)
        self.Predictive_parsing()
        self.tree = self.get_tree()


    #FIRST & FOLLOW

    def get_first(self, key: str, sub_p: dict, first: dict) -> None:
        '''
        Search First elemets of a given non terminal element
        using the rules given in page 221
        '''

        for sub_key in sub_p:
            i = sub_p[sub_key][0]
            if not 65 <= ord(i) <= 90:
                first[key].append(i)
            elif 65 <= ord(i) <= 90 and i in self.G:
                self.get_first(key, self.G[i], first)

    def First(self) -> dict:
        '''
        Create de abstraction of the First table

        Return a dict with the info
        '''
        first = dict()

        for key in self.keys:
            first[key] = list()
            self.get_first(key, self.G[key] , first)

        return first

    def search_terminal(self, sub_p) -> str:
        '''
        Search the last possible terminal produced of a
        given non termianl element

        Return the las possible terminal
        '''

        for sub_key in sub_p:
            prod = sub_p[sub_key]
            i = prod[0]
            if not 65 <= ord(i) <= 90:
                return i
            else:
                return self.search_terminal(self.G[i])
    
    def search_epsilon(self, sub_p) -> bool:
        '''
        Search if a given non terminal element 
        produce an epsilon

        return if an epsilon is found
        '''

        flag = False
        for sub_key in sub_p:
            prod = sub_p[sub_key]
            for term in prod:
                if term == 'e':
                    flag = True
            
        return flag

    def get_follow(self, search_key, follow) -> None: 
        '''
        Search Follow elemets of a given non terminal element
        using the rules given in page 221 & 222
        '''

        for key in self.keys: 
            for k in self.G[key]: 

                prod = self.G[key][k]
                for i in range(len(prod)):
                    if prod[i] == search_key:
                        if i < len(prod)-1:

                            if not 65 <= ord(prod[i+1]) <= 90:
                                if not prod[i+1] in follow[search_key]:
                                    follow[search_key].append(prod[i+1])
                            else:
                                find_term = self.search_terminal(self.G[prod[i+1]])
                                if not find_term in follow[search_key]:
                                    follow[search_key].append(find_term)
                                if self.search_epsilon(self.G[prod[i+1]]):
                                    for term in follow[key]: 
                                        if not term in follow[search_key]:
                                            follow[search_key].append(term)

                        else: 
                            for term in follow[key]:
                                if not term in follow[search_key]:
                                    follow[search_key].append(term)

    def Follow(self):
        '''
        Create de abstraction of the Follow table

        Return a dict with the info
        '''

        follow = dict()

        for k in self.keys:
            follow[k] = []
  
        follow['S'].append('$')

        for key in self.G:
            self.get_follow(key, follow)

        for key in self.G:
            self.get_follow(key, follow)

        return follow

    #PARSING TABLE

    def get_parsing_table(self) -> list:
        '''
        Construction of a predictive parsing table 
        using the rules given in page 224 & 225

        Return a list with the parsing table info
        '''

        p_table = []

        for s in self.keys:
            for t in self.G[s]:
                p_table.append([None]*len(self.terminals))
    
        for i in range(len(self.sub_keys)):
            for j in range(len(self.terminals)):
                prod = self.G[self.sub_keys[i][0]][self.sub_keys[i]]
                if not 'e' in prod:    
                    if self.terminals[j] in self.first[self.sub_keys[i][0]]:
                        if self.terminals[j] in prod:
                            p_table[i][j] = i
                
                    if 65 <= ord(prod[0]) <= 90:
                        if self.terminals[j] in self.first[prod[0]]:
                            p_table[i][j] = i
                else:
                    if self.terminals[j] in self.follow[self.sub_keys[i][0]]:
                        p_table[i][j] = i
        
        return p_table

    def Parsing_table(self) -> dict:
        '''
        Create de abstraction of the Parsing table

        Return a dict with the info
        '''

        p_table = self.get_parsing_table()
        M = dict()

        for key in self.keys:
            M[key] = [None]*len(self.terminals)
            for sub_key in self.G[key]:
                pt = p_table[self.sub_keys.index(sub_key)]
                for i in range(len(pt)):
                    if pt[i] != None:
                        M[sub_key[0]][i] = pt[i]

        return M

    #PREDICTIVE PARSING

    def Predictive_parsing(self):
        '''
        Makes the Top-Down-Parsing with the entered grammar and string
        '''

        print("\nTop Down Parsing:\n")

        i = 0
        prod = ['$']

        a = self.w[i]
        X = self.stack[-1]

        node = self.root
        childs = None
        is_S = False

        while X != '$':
            print(f'Actual Stack: {self.stack}\t\tActual Chain: {self.w}')
            if X == 'e':
                print(f'X = {X}, a = {a}\nCoincidence X=e\nPop epsilon')
                self.stack.pop()
            elif X == a:
                self.stack.pop()
                print(f'X = {X}, a = {a}\nCoincidence X=a\npop {a}')
                i += 1
                if i == len(self.w):
                    break
                a = self.w[i]
            elif X in self.terminals: 
                print(f'X = {X}\nX is terminal')
                break
            elif self.parsing_table[X][self.terminals.index(a)] == None: 
                print(f'X = {X}, a = {a}\nNot found production M[X,a] = {self.parsing_table[X][self.terminals.index(a)]}')
                break
            else: 

            
                num = self.parsing_table[X][self.terminals.index(a)]
                sub_key = self.sub_keys[num]
                prod = self.G[sub_key[0]][sub_key].copy()
            
            
                if is_S:
                    find = False
                    while not find:
                        for child in childs:
                            if X == child.X:
                                if child.childs == []: 
                                    node = child
                                    find = True
                        if not find:
                            node = node.parent
                            childs = node.childs
                is_S = True
            
            
                childs = node.get_childs(prod, node)

                print(f'X = {X}, a = {a}\nFound Produccion M[X,a] = {self.parsing_table[X][self.terminals.index(a)]}\nPush to stack: {prod}')

            
                prod.reverse()
                self.stack.pop()
                for t in prod:
                    self.stack.append(t)
            
            
            X = self.stack[-1]
            print()

        print(f'Actual Stack:{self.stack}')

    def get_tree(self):
        '''
        Create a tree representation of the derivation 
        tree of the word in the grammar
        '''
        return self.root.create_tree()

    #AUXILIAR

    def get_keys(self) -> list:
        '''
        Return a list with grammar non terminal elements
        '''
        keys = list()
        for key in self.G:
            keys.append(key)
        return keys

    def get_sub_keys(self) -> list:
        '''
        Returns a list with non-terminal grammar elements.
        and if a nonterminal has two productions, it puts 
        one element in the list for each production.

        '''
        sub_keys = list()
        for key in self.keys:
            for sub_key in self.G[key]:
                sub_keys.append(sub_key)
        return sub_keys

    def get_terminals(self) -> list:

        terminals = []

        for key in self.keys:
            for sub_key in self.G[key]:
                for term in self.G[key][sub_key]:
                    if not 65 <= ord(term) <= 90 and term != 'e':
                        terminals.append(term)
        
        terminals.append('$')
        
        return terminals

    #GRAMMAR INPUT

    def input_w(self) -> str:
        w = input('\nEnter the string to process:\n')
        w += '$'
        print("\n######################################")
        return w

    def input_grammar(self) -> dict:
        '''
        Create de abstraction of the Grammar:
        Asks the user for grammar data and create a
        dict structs whit this information

        Return the dict with the Grammar info
        '''

        G = dict()

        with open('Grammar_Input.txt') as f:
            lines = f.readlines()

        li = 0

        print("\nGrammar:")
        while True:
            prod = str(lines[li].rstrip('\n'))
            li += 1
            if prod == 'end':
                break
            elif prod != '\n':
                print(prod)
                key = prod[0]
                G[key] = {}
                prod = prod[5:]
            

            sub_prod = prod.split('|')

            i = 1
            if len(sub_prod) == 1:
                G[key][key] = []
                for x in prod:
                    G[key][key].append(x)
            else:
                for sub_p in sub_prod:
                    G[key][key+str(i)] = []
                    for x in sub_p:
                        G[key][key+str(i)].append(x)
                    i += 1
        
        return G
