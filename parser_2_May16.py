
import sys
from anytree import Node, RenderTree
from lexer import main









    
# Search for the lexer.py file in the current directory and its subdirectories
"""for root, dirs, files in os.walk('.'): 
    if 'lexer.py' in files:
        lexer_dir = os.path.abspath(root)
        break

# Change directory to where the lexer code is located
os.chdir(lexer_dir)
"""
# Run the lexer using the command-line
#os.system('python lexer.py')
class Token:
    def __init__(self, line_num, token_num, token_type):
        self.line_num = line_num
        self.token_num = token_num
        self.token_type = token_type

    def as_tuple(self):
        return self.line_num, self.token_num, self.token_type


def load_tokens_from_file(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line in file:
            line_tokens = line.strip().split()
            line_num, token_num, token_type = line_tokens[:3]
            token = Token(int(line_num), int(token_num), token_type)
            tokens.append(token)
    return tokens


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    @property
    def next_token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]

    def advance_token(self):
        
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            print(token.token_type)
            return token

    def current_token(self):
        if 0 <= self.index < len(self.tokens):
            return self.tokens[self.index]

    def lookahead_token(self):
        if self.index + 1 < len(self.tokens):
            return self.tokens[self.index + 1]

    def get_line_number(self):
        token = self.current_token()
        if token:
            return token.line_num

    def get_token_number(self):
        token = self.current_token()
        if token:
            return token.token_num

    def get_token_type(self):
        token = self.current_token()
        if token:
            return token.token_type
        
    def lookahead_type(self):
        lookahead = self.lookahead_token()
        if lookahead:
            return lookahead.token_type
        else:
            return None
     
    def backtrack_token(self):
        if self.index > 0:
            self.index -= 1
        else:
            print("Cannot backtrack further. Already at the beginning of the token stream.")


# Example usage
file_path = 'token.txt'
tokens = load_tokens_from_file(file_path)

stream = TokenStream(tokens)
# Read in the token stream from the lexer output file
def language():
    language_node = Node("language")
    functions_node = functions(language_node)
    main_body_node = Main_Body(language_node)

    if functions_node:
        functions_node.parent = language_node
    if main_body_node:
        main_body_node.parent = language_node

    return language_node


def functions(parent): # or nothing if no functions
    functions_node = Node("functions",parent=parent)
    if stream.get_token_type() == 'DEFINE': # if we dont have a function we should not check if there is still a function to read again
        additional_functions_node = functionRE(functions_node)
        Node("additional_functions", parent=functions_node)
    else:
        
        return functions_node
    
def functionRE(parent): # function return type and name
    functionRE_node = Node('functionRE',parent=parent)
    if stream.get_token_type() == 'DEFINE' and stream.lookahead_type() == 'ID':
        node_define = Node('DEFINE', parent=functionRE_node)
        stream.advance_token() # he should be in ID at this position and then verify the open parenthesis
        node_id = Node('ID', parent=functionRE_node)
        parse_functionCall(functionRE_node) # i should be in open parenthesis when i finish this function
        stream.advance_token() # i should be in open curly bracket when i finish this function
        if stream.get_token_type() == 'OPCURL':
            opcurl_node = Node('OPCURL', parent=functionRE_node)
            stream.advance_token() # i should be in ID now because i skipped the curly bracket
            statement_node = Node('statement', parent=functionRE_node)
            statement(statement_node) 
        if stream.get_token_type() == 'CLCURL':
            clcurl_node = Node('CLCURL', parent=functionRE_node)
            stream.advance_token()
            return functionRE_node
        else:   
            raise Exception("Syntax error: expected CPCURL in line {} ".format(stream.get_line_number()))
    else: 
        raise Exception("Syntax error: expected DEFINE and ID in line {} ".format(stream.get_line_number()))    
    
    
   

def statement(parent):
    statement_node = Node('statement', parent=parent)
    print("current token ", stream.get_token_type())
    
    statement_w_endl_node = None
    statements_wo_endl_node = None
    
    if stream.get_token_type() in ['ID', 'RETURN']:
        statement_w_endl_node = Node('statement_w_endl', parent=statement_node)
        statement_w_endl(statement_w_endl_node)
        
        if stream.get_token_type() == 'NEWL':
            endline_node = Node('NEWL', parent=statement_node)
            stream.advance_token()
            statement(statement_node)
        else:
            raise Exception("Syntax error: expected NEWL in line {}".format(stream.get_line_number()))
    
    elif stream.get_token_type() in ['IF', 'LOOP', 'ELSE']:
        statements_wo_endl_node = Node('statements_wo_endl', parent=statement_node)
        statements_wo_endl(statements_wo_endl_node)
        statement(statement_node)
    
   
    
    return statement_node


def statements_wo_endl(parent): # this function is taking IF or LOOP as arguments
    statements_wo_endl_node = Node('statements_wo_endl', parent=parent)
    print("current token at statements_wo_endl: ", stream.get_token_type())
    if stream.get_token_type() == 'LOOP':
       loop_node = Node('loop', parent=statements_wo_endl_node)
       loop(loop_node)
    elif stream.get_token_type() == 'IF':
        if_statement_node = Node('if_statement', parent=statements_wo_endl_node)
        if_statement(if_statement_node)
    
    return statements_wo_endl_node

def statement_w_endl(parent):
    statement_w_endl_node = Node('statement_w_endl', parent=parent)
    
    if stream.get_token_type() == 'ID':
        id_node = Node('ID', parent=statement_w_endl_node)
        if stream.lookahead_type() == 'OPPARENT':
            function_call_node = Node('function_call', parent=statement_w_endl_node)
            function_call(function_call_node)
            print("current token should be OPPARENT: ", stream.get_token_type())
        elif stream.lookahead_type() == 'ASSIGN':
            arith_op_node = Node('arith_op', parent=statement_w_endl_node)
            arith_op(arith_op_node)
        elif stream.lookahead_type() == 'OPBRACKET':
            print("current token should be OPBRACKET: ", stream.get_token_type())
            assignment_node = Node('assignmentArray', parent=statement_w_endl_node)
            AssignmentArray(assignment_node)
    elif stream.get_token_type() == 'RETURN':
        return_node = Node('return', parent=statement_w_endl_node)
        Return(return_node)
    
    return statement_w_endl_node
    



def arith_op(parent):
    arith_op_node = Node('arith_op', parent=parent)

    # even though it is stupid 
    # now I am looking at ID = ID + ID;
    if stream.get_token_type() is not None and stream.get_token_type() == 'ID':
        check_node = check(arith_op_node)
        # check already advances the token
        if stream.get_token_type() == 'ASSIGN':
            stream.advance_token()
            arith_expr_node = arith_expr(arith_op_node)
            arith_expr_node.parent = arith_op_node  # Set arith_op_node as the parent of arith_expr_node
            check_node.parent = arith_op_node  # Set arith_op_node as the parent of check_node
        else:
            raise Exception("Syntax error: expected ASSIGN in line {} ".format(stream.get_line_number()))
    else:
        raise Exception("Syntax error: expected ID in line {} ".format(stream.get_line_number()))

    return arith_op_node, arith_expr_node




def check(parent):
    check_node = Node('check', parent=parent)

    if stream.get_token_type() is not None and stream.get_token_type() == 'ID':
        id_node = Node(stream.get_token_type(), parent=check_node)
        stream.advance_token()
        id_node.parent = check_node  # Set check_node as the parent of id_node
    else:
        raise Exception("Syntax error: expected ID in line {}".format(stream.get_line_number()))

    return check_node



def arith_expr(parent):
    arith_expr_node = Node('arith_expr', parent=parent)
    term_node = term(arith_expr_node)
    arith_expr_tail_node = arith_expr_tail(arith_expr_node)

    term_node.parent = arith_expr_node  # Set arith_expr_node as the parent of term_node
    arith_expr_tail_node.parent = arith_expr_node  # Set arith_expr_node as the parent of arith_expr_tail_node

    return arith_expr_node

 



def add_op(parent):
    add_op_node = Node('add_op', parent=parent)
    if stream.get_token_type() is not None and (stream.get_token_type() == 'ADD' or stream.get_token_type() == 'SUB' or stream.get_token_type() == 'MUL' or stream.get_token_type() == 'DIV'):
        stream.advance_token()
        print("current token at add_op: ", stream.get_token_type())
    else:
        add_op_node = None  # Set add_op_node to None if the condition is not met

    return add_op_node


def arith_expr_tail(parent):
    arith_expr_tail_node = Node('arith_expr_tail', parent=parent)
    add_op_node = add_op(arith_expr_tail_node)
    if add_op_node is not None:
        term_node = term(arith_expr_tail_node)
        arith_expr_tail_node.children = [add_op_node, term_node]
        print("current token: ", stream.get_token_type())
        arith_expr_tail(arith_expr_tail_node)

    return arith_expr_tail_node



def term(parent):
    term_node = Node('term', parent=parent)
    if stream.get_token_type() is not None and stream.get_token_type() in ['NUM', 'ID']:
        print("current token: ", stream.get_token_type())
        stream.advance_token()
        print("current token: ", stream.get_token_type())
    else:
        raise Exception("Syntax error: expected ID or NUM in line {} ".format(stream.get_token_type()))
    return term_node




def parse_functionCall(parent):
    parse_function_node = Node('parse_functionCall', parent=parent)
    
    if stream.get_token_type() == 'ID':
        stream.advance_token()
        id_node = Node('ID', parent=parse_function_node)
        if stream.get_token_type() == 'OPPARENT':
            oparent_node = Node('OPPARENT', parent=parse_function_node)
            stream.advance_token()  # Skip the opening parenthesis
            
            if stream.get_token_type() != 'CLPARENT':
                parse_argument_list_node = Node('parse_argument_list', parent=parse_function_node)
                parse_argument_list(parse_function_node)
            elif stream.get_token_type() == 'CLPARENT':
                stream.advance_token()  # Skip the closing parenthesis
                return parse_function_node  # Return the parse_function_node to connect it to the syntax tree
            else:
                raise Exception("Syntax error: expected CLPARENT in line {}".format(stream.get_line_number()))
        else:
            raise Exception("Syntax error: expected OPPARENT in line {}".format(stream.get_line_number()))
    else:
        raise Exception("Syntax error: expected ID in line {}".format(stream.get_line_number()))


def parse_argument_list(parent):
    parse_argument_list_node = Node('parse_argument_list', parent=parent)
    parse_expression_node = parse_expression(parse_argument_list_node)
    parse_argument_list_node.children = [parse_expression_node]  # Parse the first expression
    
    nodeVA = variable(parse_argument_list_node)
   
        # Check if the node already exists as a child node before adding it
    nodeVA.parent = parse_argument_list_node  # Set parse_argument_list_node as the parent of nodeVA
    
    return parse_argument_list_node

"""def variable (parent):
    variable_node = Node('variable', parent=parent)
    while stream.get_token_type() == 'COMMA':
        stream.advance_token()
        parse_expression(variable_node)

    return variable_node
"""
"""def variable(parent):
    variable_node = Node('variable', parent=parent)
    expressions = ()  # Create an empty tuple to store the nodes
    
    while stream.get_token_type() == 'COMMA':
        stream.advance_token()
        node = parse_expression(variable_node)
        expressions = list(expressions)  # Convert the tuple to a list
        expressions += [node]  # Append the new node to the list
        expressions = tuple(expressions)  # Convert the list back to a tuple
    
    variable_node.children = expressions  # Set the tuple of nodes as the children of the variable node
    return variable_node
"""
def variable(parent):
    variable_node = Node('variable', parent=parent)
    expressions = ()  # Create an empty tuple to store the nodes
    
    while stream.get_token_type() == 'COMMA':
        comma_node = Node('COMMA', parent=variable_node)  # Create a new node to represent the comma
        stream.advance_token()
        parse_expression_node = Node('parse_expression', parent=variable_node)  # Create a new node to represent the parse_expression function call
        expression_node = parse_expression(parse_expression_node)  # Call the parse_expression function to parse the expression
        parse_expression_node.children = [expression_node]  # Set the expression node as the child of the parse_expression node
        expressions = list(expressions)  # Convert the tuple to a list
        expressions += [comma_node, parse_expression_node]  # Append the comma and the parse_expression node to the list
        expressions = tuple(expressions)  # Convert the list back to a tuple
    
    variable_node.children = expressions  # Set the tuple of nodes as the children of the variable node
    return variable_node

def parse_expression(parent):
    parse_expression_node = Node('parse_expression', parent=parent)
    
    if stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM']:
        expression_token = stream.get_token_type()
        expression_node = Node(expression_token, parent=parse_expression_node)
        stream.advance_token()
        return expression_node  
    else:
        raise Exception("Syntax error: expected ID or NUM in line {}".format(stream.get_line_number()))
    
   



def loop(parent):
    loop_node = Node("loop", parent=parent)
    if stream.get_token_type() == 'LOOP':
        stream.advance_token()
        condition(loop_node)
        if stream.get_token_type() != 'OPCURL':
            raise Exception("Syntax error: expected OPCURL in line {}".format(stream.get_line_number()))
        else:
            stream.advance_token()
            statement(loop_node)
            if stream.get_token_type() != 'CLCURL':
                print("Syntax error: expected CLCURL in line {}".format(stream.get_line_number()))
            else:
                stream.advance_token()
    return loop_node




def condition(parent):
    condition_node = Node("condition", parent=parent)
    if stream.get_token_type() == 'OPPARENT':
        opparent_node = Node('OPPARENT', parent=condition_node)
        stream.advance_token()
        comparisons(condition_node)
        if stream.get_token_type() != 'CLPARENT':
            raise Exception("Syntax error: expected CLPARENT in line {}".format(stream.get_line_number()))
        else:
            clparent_node = Node('CLPARENT', parent=condition_node)
            stream.advance_token()
    return condition_node




def comparisons(parent): # 
    comparisons_node = Node("comparisons", parent=parent)
    value(comparisons_node)
    valie_node = Node("value", parent=comparisons_node)
    comparison_op(comparisons_node)
    value_node = Node("value", parent=comparisons_node)
    value(comparisons_node)
    value_node = Node("value", parent=comparisons_node)
    optional_logic(comparisons_node)
    return comparisons_node



def optional_logic(parent):
    optional_logic_node = Node("optional_logic", parent=parent)

    if stream.get_token_type() in ['AND', 'OR', 'NOT']:
        optional_node = Node(stream.get_token_type(), parent=optional_logic_node)

        stream.advance_token()
        comparisons(optional_logic_node)
        optional_logic(optional_logic_node)
        
    return optional_logic_node




def comparison_op(parent):
    comparison_op_node = Node("Comparison_op", parent=parent)
    if stream.get_token_type() in ['EQU', 'SMALL', 'SMALLQUI', 'NOTEQUI']:
        comparison_op = stream.get_token_type()
        comparison_op_node = Node(comparison_op, parent=parent)
        stream.advance_token()
    else:
        raise Exception("Syntax error: expected comparison operator in line {}".format(stream.get_line_number()))
    return comparison_op_node



def value(parent):
    value_node = Node("Value", parent=parent)
    if stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM']:
        value = stream.get_token_type()
        val_node = Node(value, parent=value_node)
        val_node.parent = value_node
        print("value: ", value)
        stream.advance_token()
    else:
        raise Exception('Expected value')
    return value_node




def else_statement(parent):
    else_statement_node = Node("else_statement", parent=parent)
    
    if stream.get_token_type() == 'ELSE' and stream.lookahead_type() == 'OPCURL':
        else_node = Node("ELSE", parent=else_statement_node)
        else_node.parent = else_statement_node
        stream.advance_token()
        OPcurl_node = Node("OPCURL", parent=else_statement_node)
        OPcurl_node.parent = else_statement_node
        stream.advance_token()
        print("current token: ", stream.get_token_type())
        statement(else_statement_node)  # Call the statement function with the parent node
        if stream.get_token_type() != 'CLCURL':
            raise Exception("Syntax error: expected CLCURL in line {} ".format(stream.get_line_number()))
        else:
            CLCurl_node = Node("CLCURL", parent=else_statement_node)
            CLCurl_node.parent = else_statement_node
            stream.advance_token()
            return else_statement_node
    else:
        print("no else statement")
        return None   



def if_statement(parent):
    if_statement_node = Node("if_statement", parent=parent)
    stream.advance_token()  # Move to the next token
    print("current token: ", stream.get_token_type())
    condition_node = condition(if_statement_node)  # Assign the result of condition() to a variable
    opcurl_node = None
    if stream.get_token_type() != 'OPCURL':
        raise Exception("Syntax error: expected OPCURL in line {} ".format(stream.get_line_number()))
    else:
        opcurl_node = Node("OPCURL", parent=if_statement_node)
        opcurl_node.parent = if_statement_node

        stream.advance_token()
    
        condition_node.parent = if_statement_node  # Add the condition_node as a child of if_statement_node
        statement(if_statement_node)
        if stream.get_token_type() != 'CLCURL':
            raise Exception("Syntax error: expected CLCURL in line {} ".format(stream.get_line_number()))
        else:
            CLCurl_node = Node("CLCURL", parent=if_statement_node)
            CLCurl_node.parent = if_statement_node
            stream.advance_token()
            else_node = else_statement(if_statement_node)  # Assign the result of else_statement() to a variable
            if else_node:
                else_node.parent = if_statement_node  # Add the else_node as a child of if_statement_node
    return if_statement_node
 


def Main_Body(parent):
    main_body_node = Node("Main_Body", parent=parent)
    if stream.get_token_type() != 'BEGIN':
        print("Syntax error: expected BEGIN in line {} ".format(stream.get_line_number()))
    else:
        print("current token: ", stream.get_token_type())
        Begin_node = Node("BEGIN", parent=main_body_node)
        stream.advance_token()
       
        stream.advance_token()
        print("current token: ", stream.get_token_type())
        end_node = Node("NEWL", parent=Begin_node)
        node = statement(main_body_node)
        if stream.get_token_type() != 'END':
            print("Syntax error: expected END in line {} ".format(stream.get_line_number()))
        else:
            if stream.lookahead_type() != 'NEWL':
                raise Exception("Syntax error: expected NEWL in line {} ".format(stream.get_line_number()))
               
            else:
                end_node = Node("END", parent=main_body_node)
           
                stream.advance_token()
                endlin = stream.get_token_type()
                endline = Node(endlin, parent=end_node)

            
                print("Syntax analysis completed successfully")
                return main_body_node



def function_call(parent):
    function_call_node = Node("Function_call", parent=parent)
    stream.advance_token()  # Move to the next token
    stream.advance_token()  # Move to the ID token
    # Enter inside the arguments
    if stream.get_token_type() != 'CLPARENT':
        parse_argument_list(function_call_node)
    if stream.get_token_type() != 'CLPARENT':
        raise Exception("Syntax error: expected CLPARENT in line {} ".format(stream.get_line_number()))
    else:
        stream.advance_token()       
        return function_call_node

from anytree import Node

def array(parent):
    array_node = Node("array", parent=parent)
    size(array_node)
    size(array_node)
    return array_node



def AssignmentArray(parent):
    assignment_node = Node("AssignmentArray", parent=parent)
    if stream.get_token_type() == 'ID':
        id_node = Node(stream.get_token_type(), parent=assignment_node)
        id_node.parent = assignment_node
        stream.advance_token()
        array(assignment_node)
        if stream.get_token_type() == 'ASSIGN':
            Assignment_op_node = Node(stream.get_token_type(), parent=assignment_node)
            Assignment_op_node.parent = assignment_node
            zorto(assignment_node)
    return assignment_node



def zorto(parent):
    zorto_node = Node("zorto", parent=parent)
    stream.advance_token()
    if stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM'] and stream.lookahead_type() == 'CONCA':
        stream.advance_token()
        stream.advance_token()
        stream.advance_token()
        array(zorto_node)
    elif stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM'] and stream.lookahead_type() != 'CONCA':
        stream.advance_token()
    return zorto_node



def size(parent):
    size_node = Node("size", parent=parent)
    if stream.get_token_type() == 'OPBRACKET':
        oppbracket_node = Node(stream.get_token_type(), parent=size_node)
        oppbracket_node.parent = size_node
        stream.advance_token()
        if stream.get_token_type() in ['NUM', 'ID']:
            id_node = Node(stream.get_token_type(), parent=size_node)
            id_node.parent = size_node
            stream.advance_token()
            if stream.get_token_type() == 'CLBRACKET':
                clbracket_node = Node(stream.get_token_type(), parent=size_node)
                clbracket_node.parent = size_node
                stream.advance_token()
            else:
                raise Exception('Expected ]')
        else:
            raise Exception('Expected number')
    return size_node



def Return(parent):
    return_node = Node("Return", parent=parent)

    if stream.get_token_type() == 'RETURN':
        stream.advance_token()
        if stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM', 'FALSE', 'TRUE']:
            print("current token: ", stream.get_token_type())
            return_id = Node(stream.get_token_type(), parent=return_node)
            return_id.parent = return_node
            stream.advance_token()
        else:
            raise Exception('EXPECTED ID')
    else:
        raise Exception('EXPECTED RETURN')
    
    return return_node




main()
# Create the language node
language_node = language()

# Print the tree starting from the language node
for pre, _, node in RenderTree(language_node):
    print(f"{pre}{node.name}")


from anytree import RenderTree

# Define a function to write the tree to a text file
def write_tree_to_file(tree, filename):
    with open(filename, "w") as outfp:
        for pre, _, node in RenderTree(tree):
            if node.name is not None:
                outfp.write(f"{pre}{node.name}\n")
            else:
                outfp.write(f"{pre}INVALID NODE\n")

# Write the tree to a text file

write_tree_to_file(language_node, "tree.txt")