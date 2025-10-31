

import re; 
import os 
id_list=[]
delimiter_list =['{','}']
#list with reserved words 
reserved_list =['loop','if','else','defining','TRUE','FALSE','BEGIN','END','RETURN','wu','ag','pt','go','br','gl','st','so','no','we','ea','sc','bu','em']
#list with operators
operator_list=['+','-','*','/','|','\\' ,'=','$','<','!','&','!!','~']
#list with punctuation
punctuation_list=['.',',',';','(',')','[',']','{','}','/n']
#dictionary of tokens and token number
token_list_numbers ={ 'ID':1,'NUM':2,'CHAR':3,'COM':5,'ADD':6,'SUB':7,'MUL':8,'DIV':9,'ASSIGN':10,'EQU':11,'SMALL':12,'SMALLQUI':13,
'NOTEQUI':14,'OR':15,'AND':16,'NOT':17,'CONCA':18,'DOT':19,'COMMA':20,'ENDL':21,'OPPARENT':22,'CLPARENT':23,'OPCURL':24,'CLCURL':25,
'OPBRACKET':26,'CLBRACKET':27,'NEWL':28,'LOOP':29,'IF':30,'ELSE':31,'DEFINE':32,'TRUE':33,'FALSE':34,'BEGIN':35,'END':36,'RETURN':37,
'WU':38,'AG':39,'PT':40,'GO':41,'BR':42,'GL':43,'ST':44,'SO':45,'NO':46,'WE':47,'EA':48,'SC':49,'BU':50,'EM':51}
#symbol_table
symbol_table =['loop','if','else','defining','TRUE','FALSE','BEGIN','END','RETURN','wu','ag','pt','go','br','gl','st','so','no','we','ea','sc','bu','em']
#dictionary with lexemes and corresponding tokens
lexeme_token_reserved={'loop':'LOOP','if':'IF','else':'ELSE','defining':'DEFINE','TRUE':'TRUE','FALSE':'FALSE','BEGIN':'BEGIN','END':'END','RETURN':'RETURN','wu':'WU','ag':'AG','pt':'PT','go':'GO','br':'BR','gl':'GL','st':'ST','no':'NO','so':'SO','we':'WE','ea':'EA','sc':'SC','bu':'BU','em':'EM','ID':'ID','NUM':'NUM','CHAR':'CHAR'}
lexeme_token_operator={'#':'COM','+':'ADD','-':'SUB','*':'MUL','/':'DIV','=':'ASSIGN','$':'EQU','<':'SMALL','\\':'SMALLQUI','!':'NOTEQUI','|':'OR','&':'AND','!!':'NOT','~':'CONCA'}
lexeme_token_punctuation={'.':'DOT',',':'COMMA',';':'ENDL','(':'OPPARENT',')':'CLPARENT','{':'OPCURL','}':'CLCURL','[':'OPBRACKET',']':'CLBRACKET',';':'NEWL'}
#matching function: they check and either return error or token and token number

# Get the directory name of the script
#dir_name = os.path.dirname(__file__) 

# Join the directory name and output file name to get the full path of the output file
#output_file_path = os.path.join(dir_name, 'token.txt')

# check for number:
def check_num(digit):
    if re.match("^(0|[1-9][0-9]*)$",digit):
        return 'NUM'
    else:
         print(digit)
         return 'error: illegal number'
# check for character:
def check_char(char):
    if re.match("^[a-zA-Z]$",char):
         return 'CHAR'
    else:
         return "error: illegal character"    
# check for operator:
def check_operator(op):
    if(op in operator_list):
        return lexeme_token_operator.get(op)
    else:
         return "error illegal operator"
# check for  punctuation:
def check_punctuation(pun):
    if(pun in punctuation_list):
        return lexeme_token_punctuation.get(pun)
    else: 
        return 'error illegal'
# check for identifier + append to symbol table(if not there already):
def check_id(id):
    if re.match("^[a-zA-Z][_a-zA-z0-9]{0,20}$",id):
        if id in symbol_table:
            return 'ID'
        else:
            symbol_table.append(id)
            id_list.append(id)
            return 'ID'
    else:
        return 'illegal identifier'
# check for function identifier + append to symbol table(if not already there):
def check_fun_id(id): 
    if re.match("^[a-zA-Z][_a-zA-Z0-9]{0,20}$",id):
        if (id not in symbol_table ):
            symbol_table.append(id) 
            id_list.append(id)
        return 'ID'
    else: 
        return "illegal  identifier"
# check for reserved word:
def check_reserved(word): #word is the lexeme
    if(word in reserved_list):#check if word is in reserved list
        return lexeme_token_reserved.get(word) #return the token for that word 
#function to print to screen plus to file:
def print_to_screen_file(file,line,token,inputy): # inputy is the lexeme
    number=token_list_numbers.get(token) # get the token number
    print("Line " + str(line) + " Token " + "#" +str(number) + ": " + inputy + "\n") # write to screen
    #write file also ==> or inputy.isalpha()
    if inputy in id_list   or inputy.isnumeric(): # if inputy is an identifier or number then print the lexeme
        file.write(str(line) + " " + str(number) + " " + str(token) + " " + inputy + "\n") # write to file 
    else:
        file.write(str(line) + " " + str(number) + " " + str(token) + "\n") # write to file 
 #main function that calls all the other functions and does the work 
#file:
global line #global variable for line number

    
def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # Find all .txt files in the directory
    """
    Find all .txt files in the given directory that do not contain the string "token" in their filename.
    """
    text_files = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.txt') and 'token' not in filename and 'Concrete_tree' not in filename and 'Abstract_tree' not in filename :
            text_files.append(os.path.join(dir_path, filename))
    

    # Select the first .txt file
    if text_files:
        file_path = os.path.join(dir_path, text_files[0])
        print(f"Selected file: {file_path}")

        # Tokenize the file and write the tokens to an output file
        with open(file_path, 'r') as infp:
            output_file = open("token.txt", "w")
            line = 1
                

            while True:
                ch = infp.read(1)
                if(re.match(r'\s',ch)):
                    continue
                if(ch.isnumeric()):
                    number = ''
                    while(ch not in punctuation_list and ch not in operator_list and ch != " "):
                        number=number+ch
                        ch=infp.read(1)
                    print_to_screen_file(output_file,line,check_num(number),number)
                if(ch.isalpha()):
                    word=''
                    while(ch not in operator_list and ch not in  punctuation_list and ch!=" "):
                        word+=ch
                        ch= infp.read(1)
                    if(word in reserved_list):
                        print_to_screen_file(output_file,line,check_reserved(word),word)
                    else: 
                        print_to_screen_file(output_file,line,check_id(word),word)
                    if(word == 'defining'):
                        ch=''
                        word=''
                        ch=infp.read(1)
                        while(ch not in operator_list and ch not in  punctuation_list and ch!=" "):
                            word+=ch
                            ch=infp.read(1)
                        print_to_screen_file(output_file,line,check_fun_id(word),word)  
                if(ch  in operator_list):
                    if(ch =='!'):
                        op=''
                        op+=ch
                        ch=''
                        ch = infp.read(1)
                        op+=ch
                        if(op=='!!'):
                            print_to_screen_file(output_file,line,check_operator(op),op)
                        else:
                            op=''
                            op='!'
                            print_to_screen_file(output_file,line,check_operator(op),op)
                    else:
                        print_to_screen_file(output_file,line,check_operator(ch),ch)
                if(ch in punctuation_list):
                    print_to_screen_file(output_file,line,check_punctuation(ch),ch)
                    if( ch in delimiter_list):
                        line += 1
                if (ch == '#'):
                    infp.readline()
                    line += 1
                if (ch == ';'):
                    line += 1
                if not ch:
                    break
            output_file.close()
            infp.close()
    else:
        print("No .txt files found in the directory")

main()
print(symbol_table) # print the symbol table

    
    
