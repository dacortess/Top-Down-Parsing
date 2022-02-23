class Node:
    def __init__(self, X, node):
        self.X = X
        self.childs = []
        self.parent = node

    def get_childs(self, childs, parent):
        for child in childs:
            new_node = Node(child, parent)
            self.childs.append(new_node)
        return self.childs

    def create_tree(self):
        global tree
        if self.childs == []:
            return '[' + self.X + ']'
        else:
            var = ''
            var += '[' + self.X
            for child in self.childs:
                var += child.create_tree()
            var += ']'
            return var