
  
def get_tokens():
    with open('/Users/abdelhadimarjane/Documents/AUI_Classes/spring 2023/language and compilers/LanguagesRepository/project_part2 2/lexer_folder/testfolder - Copy/token.txt', 'r') as f:
        tokens = [tuple(line.split()[:3]) for line in f]
    return tokens

tokens = get_tokens()

global index
index = 0
def peek_token(): #returns the next token without consuming it don't increment the index
  
    if index < len(tokens):
        print(tokens[index])
        print(index)
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
    
def parse_value():
    consume_token()
    if peek_token()[2] in ['ID', 'NUM']:
        consume_token()
    else:
        raise Exception("Syntax error: expected ID or NUM in line {} ".format(peek_token()[0]))
def parse_arith_op():
    parse_variable()
    if peek_token()[2] == 'ASSIGN':
        parse_value()
        parse_arith_expr()
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

def parse_variable():
    if(peek_token()[2] == 'ID'):
        consume_token()
    else:
        raise Exception("Syntax error: expected ID in line {} ".format(peek_token()[0]))
def parse_arith_expr():
    parse_value()
    parse_arith_op_tail()

def parse_arith_op_tail():
    if peek_token()[2] in ['ADD', 'SUB', 'MUL', 'DIV']:
        
        parse_value()
        parse_arith_op_tail()
    else:
        pass

def parse_add_op():
    parse_arith_op()
    parse_value()

for i in range(len(tokens)):
    if peek_token()[2] == 'ID':
        parse_arith_op()
    else:
        print("completly parsed the arithmetcial operations")