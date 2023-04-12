def get_next_token():
    with open('project_part2 2/lexer_folder/testfolder - Copy/token.txt', 'r') as f:
        for line in f:
            line_tokens = line.split()[:3] # only take the first 3 tokens
            line_num, token_num, token_type = line_tokens
            yield (line_num, token_num, token_type)

token_generator = get_next_token()

def get_next_tuple():
    return next(token_generator, None)

'''def language(tokens):
  
    if MAIN_body(tokens):
        return True
    else:
        return False
def MAIN_body(tokens):
    
    if tokens[0][2] == "BEGIN" and tokens[1][2] == "NEWL":
       
        if(tokens[size-2][2]) == "END" and tokens[size-1][2] == "NEWL":
            return True
        else :
            return False
    else:
        return False

#def statments(tokens):
    #if tokens 


        '''