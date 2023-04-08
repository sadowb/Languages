'''

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

'''
import os
import re; 
id_list=[]
#list of delimeters used to identify delimeteters to increment line further doewn the code:
delimeter_list =['{','}']
#list of reserved words:
reserved_list =['loop','if','else','defining','TRUE','FALSE','BEGIN','END','RETURN','wu','ag','pt','go','br','gl','st','em','sc','bu','ea','we','so','no']
#list of operators==> 13 differnet operator:
operator_list=['+','-','*','/','=','$','<','!','&','!!','~','\\','|']
#list of punctioation ==> 9 different kinds of operators:
punctuation_list=['.',',',';','(',')','[',']','{','}']
#dicitionary of all tokens and their respective token number:
token_list_numbers ={ 'ID':1,'NUM':2,'ID2':4,'COM':5,'ADD':4,'SUB':5,'MUL':6,'DIV':7,'ASSIGN':8,'EQU':9,'SMALL':10,'SMALLQUI':11,
'NOTEQUI':12,'OR':13,'AND':14,'NOT':15,'CONCA':16,'DOT':17,'SEMI':18,'ENDL':19,'OPPARENT':20,'CLPARENT':21,'OPBRACE':22,'CLBRACE':23,
'OPBRACKET':24,'CLBRACKET':25,'LOOP':26,'IF':27,'ELSE':28,'DEFINE':29,'TRUE':30,'FALSE':31,'BEGIN':32,'END':33,'RETURN':34,
'WU':35,'AG':37,'PT':38,'GO':39,'BR':40,'GL':41,'ST':41,'EM':42,'SC':43,'BU':44,'EA':45,'WE':46,'SO':47,'NO':48,'ENDL':49}
#sybol_table initialized to stor reserved words
symbol_table = {'loop':'RW','if':'RW','else':'RW','defining':'RW','true':'RW','false':'RW','begin':'RW','end':'RW','return':'RW','wu':'RW','ag':'RW','pt':'RW','go':'RW','br':'RW','gl':'RW','st':'RW','em':'RW','sc':'RW','bu':'RW','ea':'RW','we':'RW','so':'RW','no':'RW'}
#dictionary with leximes and coresponding token 
lexim_token_reserved={'loop':'LOOP','if':'IF','else':'ELSE','defining':'DEFINE','TRUE':'TRUE','FALSE':'FALSE','BEGIN':'BEGIN','END':'END','RETURN':'RETURN','wu':'WU','ag':'AG','pt':'PT','go':'GO','br':'BR','gl':'GL','st':'ST','em':'EM','sc':'SC','bu':'BU','ea':'EA','we':'WE','so':'SO','no':'NO','ID':'ID','NUM':'NUM','ID2':'ID2'}
lexim_token_opearator={'$':'COM','+':'ADD','-':'SUB','*':'MUL','/':'DIV','=':'ASSIGN','$':'EQU','<':'SMALL','\\':'SMALLQUI','!':'NOTEQUI','|':'OR','&':'AND','!!':'NOT','~':'CONCA'}
lexim_token_punctuation={'.':'DOT',',':'SEMI',';':'ENDL','(':'OPPARENT',')':'CLPARENT','{':'OPBRACE','}':'CLBRACE','[':'OPBRACKET',']':'CLBRACKET'}
#matching function: they check and either return error or token 
# check for number :
def check_num(digit):
    if re.match("^(0|[1-9][0-9]*)$",digit):
        return 'NUM'
    else:
         print(digit)
         return 'error: illigal number'
  
# check for operator:
def check_operator(op):
    if(op in operator_list):
        return lexim_token_opearator.get(op)
    else:
         return "error illegal operator"
# check for  punctuation:
def check_punctuation(pun):
    if(pun in punctuation_list):
        return lexim_token_punctuation[pun]
    else: 
        return 'error illegal punctuation'
# check for indentifer + append to symbol table(if  the id is not there already) + plus returns either token or error:
def check_id(id):
    if re.match("^[a-zA-Z][_a-zA-z0-9]{0,20}$",id):
        if(id not in symbol_table):
            symbol_table[id]='ID'
            id_list.append(id)
        return 'ID'
        
    else:
        return 'illegal identifier'
# check for function indentifer + append to symbol table(if not already there) + plus returns either token or error:
def check_fun_id(id): 
    if re.match("^[a-zA-Z][_a-zA-z0-9]{0,20}$",id):
        if (id not in symbol_table ):
            #symbol_table.append(id) 
            symbol_table[id]='ID2'
            id_list.append(id)
        return 'ID2'
    else: 
        return "illegal  identifier"
    
#check if reserved word is in reserved word list and if it is it returns its respective token :
def check_reserved(word):
    if(word in reserved_list):
        return lexim_token_reserved.get(word)
    
#function to print to screen and writes into the output file:
def print_to_screen_file(file,line,token,inputy):
    number=token_list_numbers.get(token)
    print("Line " + str(line) + " Token " + "#" +str(number) + ": " + inputy + "\n")
    #write file also ==> or inputy.isalpha()
    if inputy in id_list   or inputy.isnumeric():
        file.write(str(line) + " " + str(number) + " " + str(token) + " " + inputy + "\n")
    else:
        file.write(str(line) + " " + str(number) + " " + str(token) + "\n")
#main function where the output and the input file is opened and procedes with reading charachter and tokenizing it: 
def main(file): #takes file path as an input
#file:
    global line 
    line = 1
    infp = open(file, "r") #opening the test file
    outputfile = open("output_token.txt", "w") #opening the output file
     
#case space:
    while 1==1: #loops until broken (1=1 acts as a flag)
        ch = infp.read(1)
        if(re.match('\s',ch)):#ignore space and continue reading
            continue
#case a number:
        if(ch.isnumeric()):
            number = '' 
            while(ch not in punctuation_list and ch not in operator_list and ch != " "): # continues reading until a non number is encountered
                number=number+ch # stores neach digit in number
                ch=infp.read(1)
            print_to_screen_file(outputfile,line,check_num(number),number) #send agrmument to function in order to tokenize, output in the creen and file information about the lexeme
#case charachter:
        if(ch.isalpha()):
            word=''
            while(ch not in operator_list and ch not in  punctuation_list and ch!=" "):#continues reading until a non aphabet is encountered
                word+=ch #stores each charachter in word 
                ch= infp.read(1)
            if(word in reserved_list): #case word is in reserved list
                print_to_screen_file(outputfile,line,check_reserved(word),word) #call the check_reserved function and other functions 
            else: 
                  print_to_screen_file(outputfile,line,check_id(word),word) # if its not a reserved word its a user identifier
            if(word == 'defining'): # either a function because function in our language always begins with defining
                ch=''
                word=''
                ch=infp.read(1)
                while(ch not in operator_list and ch not in  punctuation_list and ch!=" "):
                    word+=ch
                    ch=infp.read(1)
                print_to_screen_file(outputfile,line,check_fun_id(word),word) #tokenize,print,and write to file
        #case operator list:
        if(ch  in operator_list):
            if(ch =='!'): #continue reading operators until a non operator is encountered
                op=''
                op+=ch
                ch=''
                ch = infp.read(1)
                op+=ch
                if(op=='!!'): #case 1: !!
                    print_to_screen_file(outputfile,line,check_operator(op),op)
                else: #case !
                    op=''
                    op='!'
                    print_to_screen_file(outputfile,line,check_operator(op),op)
            else: #case another operator
                print_to_screen_file(outputfile,line,check_operator(ch),ch)
         #case punctuation:   
        if(ch in punctuation_list):
            print_to_screen_file(outputfile,line,check_punctuation(ch),ch)
            if( ch in delimeter_list):# if in delimiter uncrease line
               line += 1
        if (ch == '#'): #if comment ignore and uncrease line
            infp.readline()
            line += 1
        if (ch == ';'):#if ; then uncrease line
            line += 1
        
        
        if not ch: #get out of the loop once it reaches the end of file
            break
    print('\n')
    print('printing symbol table for test purposes :') # print symbol table to test if the user identifers are added in the symbol table
    print('\n')
    print(symbol_table)
    outputfile.close()
    infp.close() #close file
    
import os
#file function that test any file that you put in a specific folder and that ends with *.txt
directory_path = "C:\\Users\\benou\\Desktop\\testfolder" #provide path for folder containing code and test suite
i=0
#loop through all file of the path
for file in os.listdir(directory_path):
    #check if the file ends with ".txt"
    if file.endswith(".txt"):
        #if it does, call the main() function with the full path of the file
        file_path = os.path.join(directory_path, file)
        i=i+1
        print('___________________________________________________________') 
        print(' \n this is test number: ' ,str(i)) 
        print('___________________________________________________________') 
        print('\n')
        main(file_path)   
           