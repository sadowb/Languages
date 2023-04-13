


def get_tokens():
    with open('project_part2 2/lexer_folder/testfolder - Copy/token.txt', 'r') as f:
        tokens = [tuple(line.split()[:3]) for line in f]
    return tokens

tokens = get_tokens()
index = 0

def peek_token(): #returns the next token without consuming it don't increment the index
    global index
    if index < len(tokens):
        return tokens[index]
    else:
        return None

def consume_token(): #returns the next token and consumes it increments the index
    global index
    if index < len(tokens):
        token = tokens[index]
        index += 1
        return token
    else:
        return None

def parse_language():
    parse_main_body()
    parse_functions()
    print("Parsing complete")

def parse_functions():
    while peek_token()[2] == 'DEFINE':
        parse_function()

def parse_function():
    consume_token('DEFINE')
    consume_token('ID')
    parse_arguments()
    consume_token('OPCURL')
    parse_statements()
    consume_token('CLCURL')

def parse_main_body(): # this is done it works well
    if peek_token()[2] != 'BEGIN':
        raise Exception("Syntax error: expected BEGIN in line {} ".format(peek_token()[0]))
    else :
        consume_token()
    if peek_token()[2] != 'NEWL':
        raise Exception ("Syntax error: expected ; in line {} ".format(peek_token()[0]))
    else:
        consume_token()
        statements = parse_statements() # this is the problem i need to work on it 
    if peek_token()[2] != 'END':
        raise Exception ("Syntax error: expected END in line {} ".format(peek_token()[0]))
    else:
        consume_token()
    if peek_token()[2] != 'NEWL':
        raise Exception ("Syntax error: expected ; in line {} ".format(peek_token()[0]))
    else:
        consume_token()
        print("Parsing complete")
        
def parse_statements():
    while peek_token()[2] not in ['END', 'ELSE']:
        parse_statement()

def parse_statement():
    token_type = peek_token()[2]
    if token_type == 'ID2':
        parse_function_call()
    elif token_type == 'WHILE':
        parse_loop()
    elif token_type == 'IF':
        parse_if_statement()
    elif token_type == 'ID':
        parse_assignment()
    elif token_type == 'ARRAY':
        parse_array()
    elif token_type == 'RETURN':
        parse_return()
    elif token_type in ['ADD', 'SUB', 'MUL', 'DIV']:
        parse_arith_op()
    else:
        raise Exception("Syntax error: unexpected token {}".format(token_type))

def parse_arguments():
    consume_token('LPAREN')
    if peek_token()[2] != 'RPAREN':
        parse_argument_list()
    consume_token('RPAREN')

def parse_argument_list():
    parse_argument()
    while peek_token()[2] == 'COMMA':
        consume_token('COMMA')
        parse_argument()

def parse_argument():
    consume_token('ID')

def parse_function_call():
    consume_token('ID2')
    parse_arguments()

def parse_loop():
    consume_token('WHILE')
    parse_expr()
    consume_token('DO')
    parse_statements()
    consume_token('ENDL')

def parse_if_statement():
    consume_token('IF')
    parse_expr()
    consume_token('THEN')
    parse_statements()
    if peek_token()[2] == 'ELSE':
        consume_token('ELSE')
        parse_statements()
    consume_token('ENDIF')

def parse_assignment():
    consume_token('ID')
    if peek_token()[2] == 'LBRACKET':
        parse_array_index()
    consume_token('ASSIGN')
    parse_expr()

def parse_array():
    consume_token('ARRAY')
    consume_token('ID')
    consume_token('LBRACKET')
    parse_expr()
    consume_token('RBRACKET')

def parse_array_index():
    consume_token('LBRACKET')
    parse_expr()
    consume_token('RBRACKET')

def parse_return():
    consume_token('RETURN')
    if peek_token()[2] != 'ENDL':
        parse_value()

def parse_value():
    token_type = peek_token()[2]
    if token_type == 'NUM':
        consume_token('NUM')
    elif token_type == 'ID':
        consume_token('ID')
        if peek_token()[2] == 'LBRACKET':
            parse_array_index()
    else:
        raise Exception("Syntax error: unexpected token {}".format(token_type))

def parse_arith_op():
    parse_value()
    consume_token(peek_token()[2])
    parse_value()

def parse_expr():
    parse_value()
    while peek_token()[2] in ['ADD', 'SUB', 'MUL', 'DIV']:
        consume_token(peek_token()[2])
        parse_value()

parse_language()
        
# lfksdhjfmlsqkjdfmlsqdkjfmldsqkjfmlqsdkjfmlsqkjdfmlsqdkjfmlqsdkjfmlqsdkjfmldsqkjfmlqskjfdmqlskjfmlqsdkjfq
#mlkjsdfmlqskdjfmlkqsdjfmlqsdkjfmlkqdsjfmlkqsdjfmlksqdjfmlkqdsjfmlkjqsdfmlkjqsdmflkjqsdmlfkjqsdmlfkjqsdmlkfj
#lorenze mlkjsdfmlksjdqfmlsqdkjfmdlsqkjfmlqsdkjfmlqsdkjfmqlsdkjfmqsdlkjfmlqsdkjfmqsdlkjfmqlsdkdjfmlqsdkjflqdskj
def language():
    functions()
    main_body()

def main_body():
    match("BEGIN")
    statements()
    match("END")

def statements():
    if current_token[2] in ["ID2", "IF", "FOR", "WHILE", "VAR", "RETURN", "OP"]:
        statement()
        statements()

def statement():
    different_statement()
    match("ENDL")

def different_statement():
    if current_token[2] == "ID2":
        function_call()
    elif current_token[2] == "IF":
        if_statement()
    elif current_token[2] in ["FOR", "WHILE"]:
        loop()
    elif current_token[2] == "VAR":
        assignment()
    elif current_token[2] == "OP":
        array()
    elif current_token[2] == "RETURN":
        return_statement()
    elif current_token[2] in ["ADD", "SUB", "MUL", "DIV"]:
        arithmetic_operation()

def functions():
    if current_token[2] == "DEFINE":
        function()
        functions()

def function():
    match("DEFINE")
    match("ID")
    arguments()
    match("OPCURL")
    statements()
    match("CLCURL")

def arguments():
    if current_token[2] == "ID":
        match("ID")
        arguments()

def return_statement():
    match("RETURN")
    if current_token[2] != "ENDL":
        value()

def function_call():
    match("ID2")
    arguments()

def if_statement():
    match("IF")
    value()
    match("THEN")
    statements()
    if current_token[2] == "ELSE":
        match("ELSE")
        statements()
    match("ENDIF")

def loop():
    if current_token[2] == "FOR":
        for_loop()
    elif current_token[2] == "WHILE":
        while_loop()

def for_loop():
    match("FOR")
    match("ID")
    match("ASSIGN")
    value()
    match("TO")
    value()
    if current_token[2] == "STEP":
        match("STEP")
        value()
    match("DO")
    statements()
    match("ENDDO")

def while_loop():
    match("WHILE")
    value()
    match("DO")
    statements()
    match("ENDDO")

def assignment():
    match("VAR")
    match("ID")
    match("ASSIGN")
    value()

def array():
    match("OP")
    value()
    match("CP")

def value():
    if current_token[2] == "ID":
        match("ID")
    elif current_token[2] == "INT":
        match("INT")
    elif current_token[2] == "FLOAT":
        match("FLOAT")
    elif current_token[2] == "BOOL":
        match("BOOL")
    elif current_token[2] == "OP":
        value()
        match("CP")

def match(token_type):
    if current_token[2] == token_type:
        consume_token()
    else:
        error()