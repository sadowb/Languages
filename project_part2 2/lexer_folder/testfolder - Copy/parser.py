


def get_tokens():
    with open('/Users/abdelhadimarjane/Documents/AUI_Classes/spring 2023/language and compilers/LanguagesRepository/project_part2 2/lexer_folder/testfolder - Copy/token.txt', 'r') as f:
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
  #parse_functions()
  parse_main_body()
  print("Parsing complete")

def parse_functions():
  peek_token()[2] == 'DEFINE'
#parse_function()


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
                    return statements

def parse_statements():
    while peek_token()[2] not in ['END', 'ELSE']:
        parse_statement()

def parse_statement():
    token_type = peek_token()[2]
    if token_type == 'ID2':
        parse_function_call()
    elif token_type == 'LOOP':
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
    consume_token('NEWL')

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
    if peek_token()[2] != 'NEWL':
        parse_value()

def parse_valu():
    token_type = peek_token()[2] # it reads the next token without consuming it 
    if token_type == 'NUM':
        consume_token('NUM')
    elif token_type == 'ID':
        consume_token('ID')
        if peek_token()[2] == 'LBRACKET':
            parse_array_index()
    else:
        raise Exception("Syntax error: unexpected token {}".format(token_type))
def parse_value():
    consume_token()
    if peek_token()[2] == 'NUM':
        consume_token()
    else : 
        raise Exception("Syntax error: expected NUM in line {} ".format(peek_token()[0]))       
                    
def parse_arith_op():
    parse_variable()
    if peek_token()[2] == 'ASSIGN':
        parse_value()
        parse_operation()
        if peek_token()[2] == 'NEWL':
            consume_token()
        else : 
            raise Exception("Syntax error: expected NEWL in line {} ".format(peek_token()[0]))
        
        
def parse_operation():
    consume_token()
    if peek_token()[2] in ['ADD', 'SUB', 'MUL', 'DIV']:
        consume_token()
        parse_value()
        
def parse_expr():
    parse_value()
    while peek_token()[2] in ['ADD', 'SUB', 'MUL', 'DIV']:
        consume_token(peek_token()[2])
        parse_value()
def parse_variable():
    if(peek_token()[2] == 'ID'):
        consume_token()
    else:
        raise Exception("Syntax error: expected ID in line {} ".format(peek_token()[0]))
    
parse_language()

# lfksdhjfmlsqkjdfmlsqdkjfmldsqkjfmlqsdkjfmlsqkjdfmlsqdkjfmlqsdkjfmlqsdkjfmldsqkjfmlqskjfdmqlskjfmlqsdkjfq
#mlkjsdfmlqskdjfmlkqsdjfmlqsdkjfmlkqdsjfmlkqsdjfmlksqdjfmlkqdsjfmlkjqsdfmlkjqsdmflkjqsdmlfkjqsdmlfkjqsdmlkfj
#lorenze mlkjsdfmlksjdqfmlsqdkjfmdlsqkjfmlqsdkjfmlqsdkjfmqlsdkjfmqsdlkjfmlqsdkjfmqsdlkjfmqlsdkdjfmlqsdkjflqdskj
