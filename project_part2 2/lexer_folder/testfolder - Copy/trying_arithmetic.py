def get_tokens():
    with open('/Users/abdelhadimarjane/Documents/AUI_Classes/spring 2023/language and compilers/LanguagesRepository/project_part2 2/lexer_folder/testfolder - Copy/token.txt', 'r') as f:
        tokens = [tuple(line.split()[:3]) for line in f]
    return tokens

tokens = get_tokens()

global index
index = 0

def peek_token(): #returns the current token without consuming it
    global index
    if index < len(tokens):
        print(tokens[index])
        print(index)
        return tokens[index]
    else:
        return None
def consume_token():
    global index
    if index >= len(tokens):
        raise Exception('No more tokens to consume')
    token = tokens[index]
    index += 1
    print(token)
    return token


# example usage


def arith_op():
    if peek_token()[2] == "ID":
        consume_token()
        if peek_token()[2] == "ASSIGN":
            consume_token() # my index is still in assign 
            arith_expr()
            if peek_token()[2] == "NEWL":
               print("parse success")
               consume_token()
            else:
                raise Exception("Syntax error: expected NEWL in line {} ".format(peek_token()[0]))
               
           
def arith_expr():
    term()
    arith_expr_tail()
    
def term():

    if peek_token()[2] == "ID" or peek_token()[2] == "NUM":
        consume_token()
    else:
        raise Exception("Syntax error: expected ID or NUM in line {} ".format(peek_token()[0]))

def arith_expr_tail():
    
    if add_op() == True:
        term()
        arith_expr_tail()
    else:
        pass
    
def add_op():
    if peek_token()[2] == "ADD" or peek_token()[2] == "SUB" or peek_token()[2] == "MUL" or peek_token()[2] == "DIV":
       consume_token()
       return True
    else:
        return False

for i in range(len(tokens)):
    if len(tokens) == 0:
        # exit the loop if there are no more tokens to parse
        print("completely parsed arithmetical expression")
        break
    elif peek_token() is not None and peek_token()[2] == 'ID':
        arith_op()
        