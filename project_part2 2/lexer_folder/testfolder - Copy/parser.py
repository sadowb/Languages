


def get_tokens():
    with open('token.txt', 'r') as f:
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
  parse_functions()
  parse_main_body()
  print("Parsing complete")

  
def parse_functions():
  parse_function()
  parse_functions()


def parse_function():
  if peek_token()[2] != 'DEFINE':
    raise Exception("Syntax error: expected DEFINE in line {} ".format(peek_token()[0]))
  else :
    consume_token()
    if peek_token()[2] != 'ID':
      raise Exception("Syntax error: expected ID in line {} ".format(peek_token()[0]))
    else :
      consume_token()
      if parse_arguments() == True:
        if peek_token()[2] != 'OPCURL':
          raise Exception("Syntax error: expected OPCURL in line {} ".format(peek_token()[0]))
        else:
          consume_token()
          if parse_statements() == True:
            if peek_token()[2] != 'CLCURL':
              raise Exception("Syntax error: expected OPCURL in line {} ".format(peek_token()[0]))
            else:
              consume_token()         
              

def parse_main_body(): # this is done it works well
    if peek_token()[2] != 'BEGIN':
        raise Exception("Syntax error: expected BEGIN in line {} ".format(peek_token()[0]))
    else :
        consume_token()
        if peek_token()[2] != 'NEWL':
            raise Exception ("Syntax error: expected ; in line {} ".format(peek_token()[0]))
        else:
            consume_token()
            parse_statements() # this is the problem i need to work on it 
            if peek_token()[2] != 'END':
                raise Exception ("Syntax error: expected END in line {} ".format(peek_token()[0]))
            else:
                consume_token()
                if peek_token()[2] != 'NEWL':
                    raise Exception ("Syntax error: expected ; in line {} ".format(peek_token()[0]))
                else:
                    consume_token()
                  

def parse_statements():
  parse_statement()    
  parse_statements()

def parse_statement():
  if parse_statement_w_endl() == True:
    if peek_token()[2] != 'NEWL':
      raise Exception ("Syntax error: expected ; in line {} ".format(peek_token()[0]))
    else:
      consume_token()
  parse_statement_wo_endl()
      

def parse_statement_w_endl():
  status = False
  if parse_function_call() == True:
    status = True
  if parse_assignment() == True:
    status = True  
  if parse_array() == True:
    status = True
  if parse_return() == True:
    status = True
  if parse_arith_op() == True:
    status = True
  return status

def parse_statement_wo_endl():
  parse_loop()
  parse_if_statement()


def parse_arguments():
  if peek_token()[2] != 'OPPARENT':
      raise Exception ("Syntax error: expected ( in line {} ".format(peek_token()[0]))
    else:
      consume_token()
      parse_variables();
      if peek_token()[2] != 'CLPARENT':
        raise Exception ("Syntax error: expected ) in line {} ".format(peek_token()[0]))
      else:
        consume_token()

def parse_variables():
  parse_value()
  parse_variable()

def parse_variable():
  if peek_token()[2] != 'COMMA':
    raise Exception ("Syntax error: expected , in line {} ".format(peek_token()[0]))
  else:
    consume_token()
    parse_variables()

def parse_value():
  if peek_token()[2] != 'NUM':
    raise Exception ("Syntax error: expected NUM in line {} ".format(peek_token()[0]))
  else:
    consume_token()

def parse_condition():
  if peek_token()[2] != 'OPPARENT':
    raise Exception ("Syntax error: expected , in line {} ".format(peek_token()[0]))
  else:
    consume_token()
    parse_comparison()
  
  
  
      



def parse_function_call():
  if peek_token()[2] != 'ID2':
      raise Exception ("Syntax error: expected ID2 in line {} ".format(peek_token()[0]))
    else:
      consume_token()
      parse_arguments();

def parse_loop():


def parse_if_statement():


def parse_assignment():


def parse_array():


def parse_return():
  if peek_token()[2] != 'RETURN':
    raise Exception ("Syntax error: expected RETURN in line {} ".format(peek_token()[0]))
  else:
    consume_token()
    parse_value()
    

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


parse_language()
