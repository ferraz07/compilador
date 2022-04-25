import re

pl_reservadas = ['int', 'float', 'char', 'void', 'printf', 'scanf', 'return', 'if', 'else', 'while', 'do', 'for']

def al(arquivo, id):
    file = './saidas/' + id +'_saida_analisador_lex.txt'
    saida = open(file, 'w')
    pl = ""
    count_linhas = 0
    arquivo = arquivo.readlines()
    for linhas in arquivo:
        count_linhas += 1
        pl = ""
        index = 0
        sup = linhas
        while index < len(sup):
            if not re.findall("[ _a-zA-Z0-9\"\;,:=!<>/*\-\+\n\t]", sup[index]) or sup == '=':
                print(f'Erro encontrado pelo analisador lexico na linha {count_linhas}, token: {sup[index]}')
                exit(1)
                break
            if re.findall("[a-zA-Z_0-9]", sup[index]):
                while re.findall("[a-zA-Z_0-9]", sup[index]):
                    pl += sup[index]
                    index += 1
                    if pl in pl_reservadas:
                        saida.write(f'PALAVRA RESERVADA: {pl.upper()} - {count_linhas} {pl}\n')
                    else:
                        saida.write(f'ID: {pl.upper()} - {count_linhas} {pl}\n')
                    pl = ""
                if sup[index] == '"':
                    index +=1
                while sup[index] != '"':
                    pl += sup[index]
                    index += 1
                saida.write(f'STRING: {count_linhas} "{pl}"\n')
                pl = ""
                if re.findall("[0-9]", sup[index]):
                    while re.findall("[0-9", sup[index]) or sup[index] == ".":
                        pl += sup[index]
                        index += 1
                    if "." in pl:
                        saida.write(f'FLOAT: {count_linhas} - {pl}\n')
                    else:
                        saida.write(f'INT: {count_linhas} - {pl}\n')
                    pl = ""
                if sup[index] == "=":
                    if linhas[index + 1] == "=":
                        saida.write(f"IGUALDADE: {count_linhas} - {pl}\n")
                        index += 1
                if sup[index] == "+":
                    saida.write(f"SOMA: {count_linhas} - {pl}\n")
                if sup[index] == "-":
                    saida.write(f"SUBTRACAO: {count_linhas} - {pl}\n")
                if sup[index] == "*":
                    saida.write(f"MULTIPLICACAO: {count_linhas} - {pl}\n")
                if sup[index] == "/":
                    saida.write(f"DIVISAO: {count_linhas} - {pl}\n")
                if sup[index] == "(":
                    saida.write(f"ABRE PARENTESES: {count_linhas} - {pl}\n")
                if sup[index] == ")":
                    saida.write(f"FECHA PARENTESES: {count_linhas} - {pl}")
                if sup[index] == "{":
                    saida.write(f"ABRE CHAVES: {count_linhas} - {pl}\n")
                if sup[index] == "}":
                    saida.write(f"FECHA CHAVES: {count_linhas} - {pl}\n")
                if sup[index] == "<":
                    if linhas[index + 1] == "=":
                        saida.write(f"MENOR OU IGUAL: {count_linhas} - {pl}\n")
                        index += 1
                    else:
                        saida.write(f"MENOR QUE: {count_linhas} - {pl}\n")
                if sup[index] == ">":
                    if linhas[index + 1] == "=":
                        saida.write(f"MAIOR OU IGUAL: {count_linhas} - {pl}\n")
                        index += 1
                    else:
                        saida.write(f"MAIOR QUE: {count_linhas} - {pl}\n")
                if sup[index] == "!":
                    if linhas[index + 1] == "=":
                        saida.write(f"DIFERENTE QUE: {count_linhas} - {pl}\n") 
                        index += 1
                if sup[index] == ";":
                    saida.write(f"PONTO VIRGULA: {count_linhas} - {pl}\n")
                
    saida.write("FIM\n")
    saida.close()
    return file
                
                






