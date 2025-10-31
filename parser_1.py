
import sys
from anytree import Node, RenderTree
from lexer import main
function_definition_list = []
counter = []

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0
class Token:
    def __init__(self, line_num, token_num, token_type, token_value=None):
        self.line_num = line_num
        self.token_num = token_num
        self.token_type = token_type
        self.token_value = token_value

    def as_tuple(self):
        return self.line_num, self.token_num, self.token_type, self.token_value
    
    def __str__(self):
        return str(self.token_value), str(self.token_type), str(self.line_num), str(self.token_num)
    
def load_tokens_from_file(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line in file:
            line_tokens = line.strip().split()
            line_num, token_num, token_type = line_tokens[:3]
            token_value = line_tokens[3] if len(line_tokens) > 3 else None
            token = Token(line_num, token_num, token_type, token_value)
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
        
    def get_token_value(self):
        token = self.current_token()
        if token:
            return token.token_value
         
    def lookahead_type(self):
        lookahead = self.lookahead_token()
        if lookahead:
            return lookahead.token_type
        else:
            return None
     
 
file_path = 'token.txt'
tokens = load_tokens_from_file(file_path)

stream = TokenStream(tokens)







counte = Counter()

def add(refs, ref, var_name, value):
    if ref not in refs:
        refs[ref] = {}
    if var_name not in refs[ref]:
        refs[ref][var_name] = []
    refs[ref][var_name].append(value)
    print(refs)

def count_values(refs, ref):
    counts = {}
    if ref in refs:
        for var_name in refs[ref]:
            counts[var_name] = len(refs[ref][var_name])
    return counts
refs = {}
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
        c = stream.get_token_value()
        function_definition_list.append(c)
        a = Node(c, parent= node_id)
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
            functions(functionRE_node)
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
        b = stream.get_token_value()
        i = Node(b, parent=id_node)
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


    # now I am looking at ID = ID + ID;
    if stream.get_token_type() is not None and stream.get_token_type() == 'ID':
       # check_node = check(arith_op_node)
        # check already advances the token
        stream.advance_token()
        if stream.get_token_type() == 'ASSIGN':
            b =Node('ASSIGN', parent=arith_op_node)
            stream.advance_token()
            arith_expr_node = arith_expr(arith_op_node)
            arith_expr_node.parent = arith_op_node  # Set arith_op_node as the parent of arith_expr_node
            #check_node.parent = arith_op_node  # Set arith_op_node as the parent of check_node
        else:
            raise Exception("Syntax error: expected ASSIGN in line {} ".format(stream.get_line_number()))
    else:
        raise Exception("Syntax error: expected ID in line {} ".format(stream.get_line_number()))

    return arith_op_node, arith_expr_node






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
        id = stream.get_token_type()
        id_node = Node(id, parent=add_op_node)
        stream.advance_token()

    else:
        add_op_node = None  # Set add_op_node to None if the condition is not met

    return add_op_node


def arith_expr_tail(parent):
    arith_expr_tail_node = Node('arith_expr_tail', parent=parent)
    add_op_node = add_op(arith_expr_tail_node)
    if add_op_node is not None:
        term_node = term(arith_expr_tail_node)
        arith_expr_tail_node.children = [add_op_node, term_node]

        arith_expr_tail(arith_expr_tail_node)

    return arith_expr_tail_node



def term(parent):
    term_node = Node('term', parent=parent)
    if stream.get_token_type() is not None and stream.get_token_type() in ['NUM', 'ID']:

        id = stream.get_token_type()
        id_node = Node(id, parent=term_node)
        i = Node(stream.get_token_value(), parent=id_node)
        stream.advance_token()

    else:
        raise Exception("Syntax error: expected ID or NUM in line {} ".format(stream.get_token_type()))
    return term_node




def parse_functionCall(parent):
    parse_function_node = Node('parse_functionCall', parent=parent)
    
    if stream.get_token_type() == 'ID':
     
        global c 
        c= stream.get_token_value()
       
        stream.advance_token()
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

    
    nodeVA = variable(parse_argument_list_node)
   
   
    return parse_argument_list_node


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
        counte.increment()
        add(refs,c, stream.get_token_value(), expression_token)
        expression_node = Node(expression_token, parent=parse_expression_node)
        y = Node(stream.get_token_value(), parent=expression_node)
        stream.advance_token()
        return expression_node  
    else:
        raise Exception("Syntax error: expected ID or NUM in line {}".format(stream.get_line_number()))
    
   


def loop(parent):
    loop_node = Node("loop", parent=parent)
    if stream.get_token_type() == 'LOOP':
        loop_node = Node('LOOP', parent=loop_node)
        stream.advance_token()
        condition_node = Node ('condition', parent=loop_node)
        condition(loop_node)
        opcurl_node = Node('OPCURL', parent=loop_node)
        if stream.get_token_type() != 'OPCURL':
            raise Exception("Syntax error: expected OPCURL in line {}".format(stream.get_line_number()))
        else:
            stream.advance_token()
            statement_node = Node('statement', parent=loop_node)
            statement(loop_node)
            if stream.get_token_type() != 'CLCURL':
                print("Syntax error: expected CLCURL in line {}".format(stream.get_line_number()))
            else:
                clcurl_node = Node('CLCURL', parent=loop_node)
                stream.advance_token()
    return loop_node




def condition(parent):
    condition_node = Node("condition", parent=parent)
    if stream.get_token_type() == 'OPPARENT':
        opparent_node = Node('OPPARENT', parent=condition_node)
        stream.advance_token()
        comparisons(condition_node)
        comparisons_node = Node('comparisons', parent=condition_node)
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
    optional_logic_node = Node("optional_logic", parent=comparisons_node)
    return comparisons_node



def optional_logic(parent):
    optional_logic_node = Node("optional_logic", parent=parent)

    if stream.get_token_type() in ['AND', 'OR', 'NOT']:
        ty = stream.get_token_type()
        optional_node = Node(ty, parent=optional_logic_node)

        stream.advance_token()
        comparisons(optional_logic_node)
        comparisons_node = Node("comparisons", parent=optional_logic_node)
        optional_logic(optional_logic_node)
        optional_logic_node = Node("optional_logic", parent=optional_logic_node)
        
    return optional_logic_node




def comparison_op(parent):
    comparison_op_node = Node("Comparison_op", parent=parent)
    if stream.get_token_type() in ['EQU', 'SMALL', 'SMALLQUI', 'NOTEQUI']:
        comparison_op = stream.get_token_type()
        comparison_op_node = Node(comparison_op, parent=comparison_op_node)
        stream.advance_token()
    else:
        raise Exception("Syntax error: expected comparison operator in line {}".format(stream.get_line_number()))
    return comparison_op_node



def value(parent):
    value_node = Node("Value", parent=parent)
    if stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM']:
        value = stream.get_token_type()
        val_node = Node(value, parent=value_node)
        v = Node(stream.get_token_value(), parent=val_node)

        stream.advance_token()
    else:
        raise Exception('Expected value')
    return value_node




def else_statement(parent):
    else_statement_node = Node("else_statement", parent=parent)
    
    if stream.get_token_type() == 'ELSE' and stream.lookahead_type() == 'OPCURL':
        else_node = Node("ELSE", parent=else_statement_node)

        stream.advance_token()
        OPcurl_node = Node("OPCURL", parent=else_statement_node)

        stream.advance_token()

        statement(else_statement_node)  # Call the statement function with the parent node
        statement_node = Node("statement", parent=else_statement_node)
        if stream.get_token_type() != 'CLCURL':
            raise Exception("Syntax error: expected CLCURL in line {} ".format(stream.get_line_number()))
        else:
            CLCurl_node = Node("CLCURL", parent=else_statement_node)

            stream.advance_token()
            return else_statement_node
    else:
        print("no else statement")
        return None   



def if_statement(parent):
    if_statement_node = Node("if_statement", parent=parent)
    if_st = stream.get_token_type()
    if_node = Node(if_st, parent=if_statement_node)
    stream.advance_token()  # Move to the next token

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
        statement_node = Node("statement", parent=if_statement_node)
        if stream.get_token_type() != 'CLCURL':
            raise Exception("Syntax error: expected CLCURL in line {} ".format(stream.get_line_number()))
        else:
            CLCurl_node = Node("CLCURL", parent=if_statement_node)
            CLCurl_node.parent = if_statement_node
            stream.advance_token()
            else_node = else_statement(if_statement_node)  # Assign the result of else_statement() to a variable
            if else_node:
                else_node = Node("else_statement",parent = if_statement_node)  # Assign the result of else_statement() to a variable

    return if_statement_node
 


def Main_Body(parent):
    main_body_node = Node("Main_Body", parent=parent)
    if stream.get_token_type() != 'BEGIN':
        raise Exception("syntax error: expected BEGIN in line {}".format(stream.get_line_number()))
    
    else:
        print("current token: ", stream.get_token_type())
        Begin_node = Node("BEGIN", parent=main_body_node)
        stream.advance_token()

        stream.advance_token()
        print("current token: ", stream.get_token_type())
        end_node = Node("NEWL", parent=Begin_node)
        node = statement(main_body_node)
        if stream.get_token_type() != 'END':
            raise Exception("Syntax error: expected END in line {} ".format(stream.get_line_number()))  
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

        i = stream.get_token_type()
        id_node = Node(i, parent=assignment_node)
        b = Node(stream.get_token_value(), parent=id_node)
        stream.advance_token()
        array(assignment_node)
        if stream.get_token_type() == 'ASSIGN':
            a = stream.get_token_type()
            Assignment_op_node = Node(a, parent=assignment_node)
            
            zorto(assignment_node)
    return assignment_node



def zorto(parent):
    zorto_node = Node("zorto", parent=parent)
    stream.advance_token()
    if stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM'] and stream.lookahead_type() == 'CONCA':
        i = stream.get_token_type()
        id_node = Node(i, parent=zorto_node)
        b = Node(stream.get_token_value(), parent=id_node)
        stream.advance_token()
        conca = stream.get_token_type()
        conca_node = Node(conca, parent=zorto_node)
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
        reurnD = stream.get_token_type()
        retu_node = Node(reurnD, parent=return_node)
        stream.advance_token()
        if stream.get_token_type() in ['NUM', 'ID', 'WU', 'AG', 'PT', 'GO', 'BR', 'GL', 'ST', 'SO', 'NO', 'WE', 'EA', 'SC', 'BU', 'EM', 'FALSE', 'TRUE']:
            print("current token: ", stream.get_token_type())
            t = stream.get_token_type()
            return_id = Node(t, parent=retu_node)
           
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

write_tree_to_file(language_node, "Concrete_tree.txt")