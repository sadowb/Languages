def get_next_token():
    with open('project_part2 2/lexer_folder/testfolder - Copy/token.txt', 'r') as f:
        for line in f:
            line_tokens = line.split()[:3] # only take the first 3 tokens
            line_num, token_num, token_type = line_tokens
            yield (line_num, token_num, token_type)

token_generator = get_next_token()

def get_next_tuple():
    return next(token_generator, None)

def parse_variable():
    token = get_token()
    if token[2] == 'ID':
        return
    elif token[2] == 'ID' and get_token()[2] == 'LBRACKET':
        parse_expr()
        if get_token()[2] != 'RBRACKET':
            raise Exception("Syntax error: expected ']' but got {}".format(token[2]))
    else:
        raise Exception("Syntax error: unexpected token {}".format(token[2]))

def parse_array():
    token = get_token()
    if token[2] == 'ID':
        token = get_token()
        if token[2] == 'LBRACKET':
            parse_expr()
            token = get_token()
            if token[2] != 'RBRACKET':
                raise Exception("Syntax error: expected ']' but got {}".format(token[2]))
        else:
            raise Exception("Syntax error: expected '[' but got {}".format(token[2]))
    else:
        raise Exception("Syntax error: expected 'ID' but got {}".format(token[2]))

def parse_expr():
    parse_value()
    parse_op()
    parse_value()

def parse_op():
    token = get_token()
    if token[2] not in ['ADD', 'SUB', 'MUL', 'DIV']:
        raise Exception("Syntax error: unexpected token {}".format(token[2]))

def parse_value():
    token = get_token()
    if token[2] != 'NUM':
        raise Exception("Syntax error: unexpected token {}".format(token[2]))

def parse_division():
    token = get_token()
    if token[2] == 'DIV':
        parse_value()
    else:
        raise Exception("Syntax error: unexpected token {}".format(token[2]))

def parse_multiplication():
    token = get_token()
    if token[2] == 'MUL':
        parse_value()
    else:
        raise Exception("Syntax error: unexpected token {}".format(token[2]))

def parse_subtraction():
    token = get_token()
    if token[2] == 'SUB':
        parse_value()
    else:
        raise Exception("Syntax error: unexpected token {}".format(token[2]))

def parse_operation():
    token = get_token()
    if token[2] == 'ADD':
        parse_value()
    else:
        parse_subtraction()

def parse_operations():
    parse_operation()
    token = get_token()
    if token[2] in ['ADD', 'SUB']:
        parse_operations()
        put_back_token(token)

def parse_arith_op():
    parse_variable()
    token = get_token()
    if token[2] != 'ASSIGN':
        raise Exception("Syntax error: expected '=' but got {}".format(token[2]))
    parse_value()
    parse_operations()

# Start parsing with the first token
get_token()
parse_arith_op()

# Check for semicolon at the end of the expression
token = get_token()
if token[2] != 'SEMICOLON':
    raise Exception("Syntax error: expected ';' but got {}".format(token[2]))

# Check for end of file
token = get_token()
if token[2] != 'EOF':
    raise Exception("Syntax error: unexpected token {}".format(token[2]))

