from anytree import Node, RenderTree
from parser_1 import language_node
from anytree import PreOrderIter

class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class SymbolTable:
    def __init__(self):
        self.symbols = {}
    
    def insert(self, symbol):
        self.symbols[symbol.name] = symbol
    
    def lookup(self, name):
        return self.symbols.get(name)
    

# select the tokens that you want to keep in the tree and remove the rest
update_tree = ['NUM','AND','OR','NOT','SMALL','EQU','RETURN','IF','ELSE','NEWL','CLCURL','CLPARENT', 'SMALLQUI', 'NOTEQUI', 'ASSIGN', 'ID', 'LOOP', 'OPCURL', 'COMMA', 'OPPARENT', 'OPBRACKET', 'ADD', 'SUB', 'MUL', 'DIV', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM','END','CONCA','BEGIN','DEFINE','TRUE','FALSE', 'statement_w_endl','statements_wo_endl']
# Create the tree using AnyTree

def reduce_tree(node, tokens):
    if not node.children:
        return node

    new_children = []
    for child in node.children:
        if child.name in tokens or child.name in ['ID', 'NUM']:
            new_child = reduce_tree(child, tokens)
            new_children.append(new_child)
        else:
            new_child = reduce_tree(child, tokens)
            new_children += new_child.children

    node.children = new_children
    return node

def update_tokens(root, tokens):
    new_tokens = tokens.copy()
    for node in PreOrderIter(root):
        if node.name == 'ID' or node.name == 'NUM':
            for child in node.children:
                if child.name not in new_tokens:
                    new_tokens.append(child.name)
    return new_tokens
g = update_tokens(language_node, update_tree)
root = reduce_tree(language_node,g)

# Print the reduced tree using AnyTree
for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.name))

def write_tree_to_file(tree, filename):
    with open(filename, "w") as outfp:
        for pre, _, node in RenderTree(tree):
            if node.name is not None:
                outfp.write(f"{pre}{node.name}\n")
            else:
                outfp.write(f"{pre}INVALID NODE\n")

def count_function_calls(root):
    function_calls = 0
    for node in PreOrderIter(root):
        if node.name == 'DEFINE':
            for child in node.children:
                if child.name == 'ID':
                    function_calls += 1
                elif child.name == 'CLPARENT':
                    return function_calls
    return function_calls

# Write the tree to a text file
def reduce_tre(root, tokens):
    reduced_children = []
    for child in root.children:
        if child.name in tokens:
            reduced_children.append(child)
        else:
            reduced_children.extend(reduce_tree(child, tokens))
    root.children = reduced_children
    return [root] + reduced_children
    
write_tree_to_file(language_node, "Abstract_tree.txt")

# if you want to change the tokens that you want to keep in the tree, change the list below
# update_tree = ['NUM','AND','OR','NOT','SMALL','EQU','RETURN','IF','ELSE','NEWL','CLCURL','CLPARENT', 'SMALLQUI', 'NOTEQUI', 'ASSIGN', 'ID', 'LOOP', 'OPCURL', 'COMMA', 'OPPARENT', 'OPBRACKET', 'ADD', 'SUB', 'MUL', 'DIV', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM','END','CONCA','BEGIN','DEFINE','TRUE','FALSE', 'statement_w_endl','statements_wo_endl']


