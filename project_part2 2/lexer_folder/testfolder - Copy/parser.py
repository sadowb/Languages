
with open('project_part2 2/lexer_folder/testfolder - Copy/token.txt', 'r') as f:
    tokens = [(line_num,) + tuple(tokens[:3]) for line_num, *tokens in map(str.split, f)]
    print(tokens)



