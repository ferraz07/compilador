from sintatico import sintatico
import re

pl_reservadas = ["int", 'float', 'char', 'void', 'printf',
                 'scanf', 'return', 'if', 'else', 'while', 'do', 'for']


er_id = re.compile(r'([a-zA-Z]+[0-9]*)')
er_aritmetica = re.compile(r'([+][+]?|--?|=|[*]|/)')
er_logica = re.compile(r'(<=?|>=?|==|!=)')
er_numero = re.compile(r'(\d+)$')
er_especial = re.compile(r'(\[|\]|\"|\(|\)|\{|\}|;|##?)')
er_separadores = re.compile(r'\s')


def lexico(arquivo, iden):
    file = './saidas/' + iden + '_saida_lexico.txt'
    saida = open(file, 'w')
    palavra = ""
    palavraOK = ""
    tipo = 0
    vetorTokens = list()
    vetorId = list()
    count_carac = 0
    count_linhas = 0
    sentinela = 0
    aspas_presentes = 0
    index_auxiliar = 0
    arquivo = arquivo.readlines()
    for line in arquivo:
        line = line.rstrip('\n')
        index = 0
        count_linhas += 1
        for index in range(len(line)):
            if aspas_presentes != 0 and index_auxiliar != 0:
                if index == index_auxiliar:
                    index_auxiliar = 0
            else:
                if line[index] != " ":
                    palavra = palavra + line[index]
                    count_carac += 1
                    if count_carac == 1:
                        sentinela = index
                        if re.findall(er_numero, line[index]):
                            palavraOK = palavra
                            #tipo = 1
                            if re.match(er_separadores, line[index + 1]) != None or re.match(er_aritmetica, line[index + 1]) != None or re.match(er_logica, line[index + 1]) != None:
                                saida.write(
                                    f"NUMERO: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                                count_carac = 0
                                palavra = ""
                                tipo = 1
                                vetorTokens.append(tipo)
                        elif re.findall(er_logica, line[index]):
                            palavraOK = palavra
                            #tipo = 6
                            if re.match(er_separadores, line[index + 1]) != None or re.match(er_aritmetica, line[index + 1]) != None or re.match(er_logica, line[index + 1]) != None:
                                saida.write(
                                    f"EX.LOGICA: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                                count_carac = 0
                                palavra = ""
                                tipo = 6
                                vetorTokens.append(tipo)
                        elif re.findall(er_aritmetica, line[index]):
                            palavraOK = palavra
                            #tipo = 5
                            if re.match(er_separadores, line[index + 1]) != None or re.match(er_aritmetica, line[index + 1]) != None or re.match(er_logica, line[index + 1]) != None:
                                saida.write(
                                    f"EX. ARITMETICA: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                                count_carac = 0
                                palavra = ""
                                tipo = 5
                                vetorTokens.append(tipo)
                        elif line[index] == '"':
                            index += 1
                            while line[index] != '"':
                                palavra += line[index]
                                palavraOK = palavra
                                index += 1
                            palavraOK = palavra + line[index]
                            #tipo = 10
                            saida.write(f"STRING: '{palavraOK}' - linha: {count_linhas} - coluna: {sentinela}\n")
                            palavra = ""
                            count_carac = 0
                            aspas_presentes = 1
                            index_auxiliar = index
                            tipo = 10
                            vetorTokens.append(tipo)
                        elif re.findall(er_especial, line[index]):
                            palavraOK = palavra
                            tipo = 4
                            if palavraOK == "(":
                                tipo = 11
                            elif palavraOK == ")":
                                tipo = 12
                            elif palavraOK == "{":
                                tipo = 13
                            elif palavraOK == "}":
                                tipo = 14
                            elif palavraOK == ";":
                                tipo = 15
                            saida.write(
                                f"CARAC. ESPECIAL: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                            count_carac = 0
                            palavra = ""
                            vetorTokens.append(tipo)
                            #receber_token(tipo, line)
                        elif re.findall(er_id, line[index]):
                            palavraOK = palavra
                            tipo = 3
                        else:
                            print(
                                f"\nErro lexico encontrado na linha: {count_linhas} e coluna: {sentinela}, token: {palavra}\n")
                            count_carac = 0
                            index += 1
                            palavra = ""
                    elif count_carac == 2:
                        if re.findall(er_numero, palavra):
                            palavraOK = palavra
                            #tipo = 1
                            saida.write(
                                f"NUMERO: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                            count_carac = 0
                            palavra = ""
                            tipo = 1
                            vetorTokens.append(tipo)
                            #receber_token(tipo, line)
                        elif re.findall(er_logica, palavra):
                            palavraOK = palavra
                            #tipo = 6
                            saida.write(
                                f"EX. LOGICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                            count_carac = 0
                            palavra = ""
                            tipo = 6
                            vetorTokens.append(tipo)
                            #receber_token(tipo, line)
                        elif re.findall(er_aritmetica, palavra):
                            palavraOK = palavra
                            #tipo = 5
                            saida.write(
                                f"EX. ARITMETICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                            count_carac = 0
                            palavra = ""
                            tipo = 5
                            vetorTokens.append(tipo)
                            #receber_token(tipo, line)
                        elif palavra in pl_reservadas:
                            palavraOK = palavra
                            tipo = 2
                            if palavraOK == "for":
                                tipo = 8
                            elif palavraOK == "if":
                                tipo = 7
                            elif palavraOK == "while":
                                tipo = 9
                            elif palavraOK == "else":
                                tipo = 17
                            saida.write(
                                f"PALAVRA RESERVADA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                            count_carac = 0
                            palavra = ""
                            vetorTokens.append(tipo)
                            #receber_token(tipo, line)
                        elif re.findall(er_id, line[index]):
                            palavraOK = palavra
                            if re.match(er_separadores, line[index + 1]) != None or re.match(er_aritmetica, line[index + 1]) != None or re.match(er_logica, line[index + 1]) != None:
                                palavraOK = palavra
                                vetorId.append(palavraOK)
                                saida.write(
                                    f"ID: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                                count_carac = 0
                                palavra = ""
                                tipo = 3
                                vetorTokens.append(tipo)
                                #receber_token(tipo, line)
                        else:
                            count_carac = 0
                            palavra = line[index]
                    elif count_carac >= 3:
                        if re.findall(er_numero, palavra):
                            palavraOK = palavra
                        elif palavra in pl_reservadas:
                            palavraOK = palavra
                            tipo = 2
                            if palavraOK == "for":
                                tipo = 8
                            elif palavraOK == "if":
                                tipo = 7
                            elif palavraOK == "while":
                                tipo = 9
                            elif palavraOK == "else":
                                tipo = 17
                            saida.write(
                                f"PALAVRA RESERVADA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                            count_carac = 0
                            palavra = ""
                            vetorTokens.append(tipo)
                            #receber_token(tipo, line)
                        elif re.findall(er_id, palavra):
                            palavraOK = palavra
                    else:
                        print(
                            f"Erro lexico encontrado na linha: {count_linhas}, token: {palavra}\n")
                        count_carac = 0
                        index += 1
                        palavra = ""
                else:
                    if re.match(er_separadores, line[index]) == " ":
                        palavra = ""
                        count_carac = 0
                    if re.findall(er_aritmetica, palavra):
                        palavraOK = palavra
                        #tipo = 5
                        saida.write(
                            f"EX. ARITMETICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                        tipo = 5
                        vetorTokens.append(tipo)
                    elif re.findall(er_logica, palavra):
                        palavraOK = palavra
                        #tipo = 6
                        saida.write(
                            f"EX. LOGICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                        tipo = 6
                        vetorTokens.append(tipo)
                    elif re.findall(er_id, palavra):
                        palavraOK = palavra
                        vetorId.append(palavraOK)
                        #tipo = 3
                        saida.write(
                            f"ID: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                        tipo = 3
                        vetorTokens.append(tipo)
                    elif re.findall(er_especial, palavra):
                        palavraOK = palavra
                        #tipo = 4
                        if palavraOK == "(":
                            tipo = 11
                        elif palavraOK == ")":
                            tipo = 12
                        elif palavraOK == "{":
                            tipo = 13
                        elif palavraOK == "}":
                            tipo = 14
                        elif palavraOK == ";":
                            tipo = 15
                        saida.write(
                            f"CARAC ESPECIAL: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                        vetorTokens.append(tipo)
                    elif re.findall(er_numero, palavra):
                        if re.match(er_separadores, line[index + 1]) != None:
                            palavraOK = palavra
                            #tipo = 1
                            saida.write(
                                f"NUMERO: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                            count_carac = 0
                            palavra = ""
                            tipo = 1
                            vetorTokens.append(tipo)
                    elif palavra in pl_reservadas:
                        palavraOK = palavra
                        tipo = 2
                        if palavraOK == "for":
                            tipo = 8
                        elif palavraOK == "if":
                            tipo = 7
                        elif palavraOK == "while":
                            tipo = 9
                        elif palavraOK == "else":
                            tipo = 17
                        saida.write(
                            f"PALAVRA RESERVADA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                        vetorTokens.append(tipo)
                    count_carac = 0
                    #vetorTokens.append(tipo)
                    #print(f"tipo pl.4: {tipo}\n")
    sintatico(iden,vetorTokens,vetorId)
                    #receber_token(tipo, line)
