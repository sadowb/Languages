'''
Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

'''

import re; 
id_list=[]
delimiter_list =['{','}']
#list with reserved words 
reserved_list =['loop','if','else','defining','TRUE','FALSE','BEGIN','END','RETURN','wu','ag','pt','go','br','gl','st','so','no','we','ea','sc','bu','em']
#list with operators
operator_list=['+','-','*','/','|','\\' ,'=','$','<','!','&','!!','~']
#list with punctuation
punctuation_list=['.',',',';','(',')','[',']','{','}','/n']
#dictionary of tokens and token number
token_list_numbers ={ 'ID':1,'NUM':2,'CHAR':3,'ID2':4,'COM':5,'ADD':4,'SUB':5,'MUL':6,'DIV':7,'ASSIGN':8,'EQU':9,'SMALL':10,'SMALLQUI':11,
'NOTEQUI':12,'OR':13,'AND':14,'NOT':15,'CONCA':16,'DOT':17,'SEMI':18,'ENDL':19,'OPPARENT':20,'CLPARENT':21,'OPBRACE':22,'CLBRACE':23,
'OPBRACKET':24,'CLBRACKET':25,'NEWL':26,'LOOP':27,'IF':28,'ELSE':29,'DEFINE':30,'TRUE':31,'FALSE':32,'BEGIN':33,'END':34,'RETURN':35,
'WU':36,'AG':37,'PT':38,'GO':39,'BR':40,'GL':41,'ST':42,'SO':43,'NO':44,'WE':45,'EA':46,'SC':47,'BU':48,'EM':49}
#symbol_table
symbol_table =['loop','if','else','defining','TRUE','FALSE','BEGIN','END','RETURN','wu','ag','pt','go','br','gl','st','so','no','we','ea','sc','bu','em']
#dictionary with lexemes and corresponding tokens
lexeme_token_reserved={'loop':'LOOP','if':'IF','else':'ELSE','defining':'DEFINE','TRUE':'TRUE','FALSE':'FALSE','BEGIN':'BEGIN','END':'END','RETURN':'RETURN','wu':'WU','ag':'AG','pt':'PT','go':'GO','br':'BR','gl':'GL','st':'ST','no':'NO','so':'SO','we':'WE','ea':'EA','sc':'SC','bu':'BU','em':'EM','ID':'ID','NUM':'NUM','CHAR':'CHAR','ID2':'ID2'}
lexeme_token_operator={'#':'COM','+':'ADD','-':'SUB','*':'MUL','/':'DIV','=':'ASSIGN','$':'EQU','<':'SMALL','\\':'SMALLQUI','!':'NOTEQUI','|':'OR','&':'AND','!!':'NOT','~':'CONCA'}
lexeme_token_punctuation={'.':'DOT',',':'SEMI',';':'ENDL','(':'OPPARENT',')':'CLPARENT','{':'OPBRACE','}':'CLBRACE','[':'OPBRACKET',']':'CLBRACKET',';':'NEWL'}
#matching function: they check and either return error or token and token number
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
    if re.match("^[a-zA-Z][_a-zA-z0-9]{0,20}$",id):
        if (id not in symbol_table ):
            symbol_table.append(id) 
            id_list.append(id)
        return 'ID2'
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
line = 1 
infp = open("/Users/abdelhadimarjane/Documents/AUI_Classes/spring 2023/language and compilers/LanguagesRepository/project_part2 2/lexer_folder/testfolder - Copy/Test2.txt", "r")#opening the test files
output_file = open("output_token.txt", "w")#opening the output file
     
    #case: space
while 1==1: #while loop to read the file character by character 
        ch = infp.read(1) #read one character at a time 
        if(re.match('\s',ch)):  #if the character is a space then continue 
            continue #continue to the next character 
    #case: a number
        if(ch.isnumeric()):#
            number = '' #empty string to store the number 
            while(ch not in punctuation_list and ch not in operator_list and ch != " "): # it reads numbers and letters until it finds a space or a punctuation or an operator
                number=number+ch # concatenate the number with the character 
                ch=infp.read(1) # retrun the next character
            print_to_screen_file(output_file,line,check_num(number),number)
#case character
        if(ch.isalpha()): #if the character is a letter then it is an identifier or a reserved word 
            word=''
            while(ch not in operator_list and ch not in  punctuation_list and ch!=" "): # it reads numbers and letters until it finds a space or a punctuation or an operator 
                word+=ch # concatenate the word with the character
                ch= infp.read(1) # read the next character
            if(word in reserved_list): # if the word is a reserved word then print it
                print_to_screen_file(output_file,line,check_reserved(word),word) # print to screen and file
            else: 
                print_to_screen_file(output_file,line,check_id(word),word) # print to screen and file
            if(word == 'defining'): # if the word is defining then it is a function identifier
                ch='' # empty the character
                word='' # empty the word
                ch=infp.read(1) # read the next character
                while(ch not in operator_list and ch not in  punctuation_list and ch!=" "): # it reads numbers and letters until it finds a space or a punctuation or an operator
                    word+=ch # concatenate the word with the character
                    ch=infp.read(1) # read the next character
                print_to_screen_file(output_file,line,check_fun_id(word),word)  
        if(ch  in operator_list): # if the character is an operator then print it
            if(ch =='!'):
                op=''
                op+=ch
                ch=''
                ch = infp.read(1)
                op+=ch # concatenate the operator with the character 
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
        
        
        if not ch: #get out of the loop once it reaches the end of file
            break
print(symbol_table) # print the symbol table
output_file.close() # close the output file
infp.close() 
    
    
#main()
#def run_tests(test_files):
    #for i, test_file in enumerate(test_files):
        #print(f"Running test {i+1}: {test_file}")
       # main(test_file) # call the main() function with the test file
        #expected_output_file = f"{test_file}.expected"
        #output_file = "output_token.txt"
        #if filecmp.cmp(expected_output_file, output_file):
            #print("Test passed!")
        #else:
            #print("Test failed. Output does not match expected output.")

#test_files = ["test1.txt", "test2.txt", "test3.txt"]
#run_tests(test_files)  
# import os

#def main(file_name):
    # Your function logic here
    #pass

# Change the directory path below to the directory where your files are located
'''import os
# write me a code that reads all the files in a folder and call the main function for each file 
directory_path = "/Users/abdelhadimarjane/Documents/AUI_Classes/spring 2023/project_part2 2/lexer_folder/"

# Loop through all files in the directory
for file in os.listdir(directory_path):
    # Check if the file ends with ".txt"
    if file.endswith(".txt"):
        # If it does, call the main() function with the full path of the file
        file_path = os.path.join(directory_path, file)
        main(file_path)  ''' 
 # call the main function
        