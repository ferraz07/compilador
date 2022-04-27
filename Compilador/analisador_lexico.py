from itertools import count
import re

pl_reservadas = ["int", 'float', 'char', 'void', 'printf', 'scanf', 'return', 'if', 'else', 'while', 'do', 'for', 'main']



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
    count_carac = 0
    count_linhas = 0
    sentinela = 0
    arquivo = arquivo.readlines() 
    for line in arquivo:
        line = line.rstrip('\n')
        index = 0
        count_linhas += 1
        for index in range(len(line)):
            #palavra = palavra + line[index]
            #print(palavraOK + "1")
            if line[index] != " ":
                palavra = palavra + line[index]
                count_carac += 1
                print(count_carac)
                print("palavra:" + palavra)
                #palavra = palavra + line[index]
                if count_carac == 1:
                    sentinela = index
                    if re.findall(er_numero, line[index]):
                        palavraOK = palavra
                        tipo = 1
                        if re.match(er_separadores, line[index +1]) != None:
                            saida.write(f"NUMERO: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                            count_carac = 0
                            palavra = ""
                    elif re.findall(er_logica, line[index]):
                        palavraOK = palavra
                        if re.match(er_separadores, line[index + 1]) != None:
                            saida.write(f"EX.LOGICA: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                            count_carac = 0
                            palavra = ""
                    elif re.findall(er_aritmetica, line[index]):
                        palavraOK = palavra
                        if re.match(er_separadores, line[index +1]) != None:
                            saida.write(f"EX. ARITMETICA: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                            count_carac = 0
                            palavra = ""
                    elif re.findall(er_especial, line[index]):
                        palavraOK = palavra
                        saida.write(f"CARAC. ESPECIAL: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                        count_carac = 0
                        palavra = ""
                    elif re.findall(er_id, line[index]):
                        palavraOK = palavra
                    else: 
                        print(f"Erro encontrado na linha {count_linhas}, token: {palavra}\n")
                        count_carac = 0
                        index+=1
                        palavra = ""
                elif count_carac == 2:
                    print(f"palavra {index}: " + palavra)
                    if re.findall(er_numero, palavra):
                        print("ENTREI NUMERO")
                        palavraOK = palavra
                        #if re.match(er_separadores, line[index + 1]) != None:
                        saida.write(f"NUMERO: {palavraOK} - linha: {count_linhas} - coluna: {sentinela}\n")
                        count_carac = 0
                        palavra = ""
                    elif re.findall(er_logica, palavra):
                        print("ENTREI logica")
                        palavraOK = palavra
                        saida.write(f"EX. LOGICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                    elif re.findall(er_aritmetica, palavra):
                        print("ENTREI arit")
                        palavraOK = palavra
                        saida.write(f"EX. ARITMETICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                    elif palavra in pl_reservadas:
                        print("ENTREI reservadas")
                        palavraOK = palavra
                        saida.write(f"PALAVRA RESERVADA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                    elif re.findall(er_id, line[index]):
                        print("ENTREI id")
                        palavraOK = palavra
                        if re.match(er_separadores, line[index + 1]) != None:
                            palavraOK = palavra
                            saida.write(f"ID: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                            count_carac = 0
                            palavra = ""
                    else: 
                        count_carac = 0
                        palavra = line[index]
                elif count_carac >= 3:
                    print("ENTREI NO ELSE 3") 
                    if re.findall(er_numero, palavra):
                        palavraOK = palavra
                    elif palavra in pl_reservadas:
                        palavraOK = palavra
                        saida.write(f"PALAVRA RESERVADA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = "" 
                    elif re.findall(er_id, palavra):
                        print(re.findall(er_id, palavra))
                        print("AQUI  COLOCAMOS")
                        palavraOK = palavra  
                else:
                    print(f"Erro encontrado na linha: {count_linhas}, token: {palavra}\n")
                    count_carac = 0
                    index +=1
                    palavra = ""     
            else:
                print("entrei no else final")
                if re.match(er_separadores, line[index]) == " ":
                    palavra = ""
                    count_carac = 0
                if re.findall(er_aritmetica, palavra):
                    palavraOK = palavra
                    saida.write(f"EX. ARITMETICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                    count_carac = 0
                    palavra = ""
                elif re.findall(er_logica, palavra):
                    palavraOK = palavra
                    saida.write(f"EX. LOGICA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                    count_carac = 0
                    palavra = ""
                elif re.findall(er_id, palavra):
                    palavraOK = palavra
                    saida.write(f"ID: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                    count_carac = 0
                    palavra = ""
                elif re.findall(er_especial, palavra):
                    palavraOK = palavra
                    saida.write(f"CARAC ESPECIAL: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                    count_carac = 0
                    palavra = ""
                elif re.findall(er_numero, palavra):
                    if re.match(er_separadores, line[index + 1]) != None:
                        palavraOK = palavra
                        saida.write(f"NUMERO: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                        count_carac = 0
                        palavra = ""
                elif palavra in pl_reservadas:
                    palavraOK = palavra
                    saida.write(f"PALAVRA RESERVADA: {palavraOK} - linha: {count_linhas} - coluna: {index}\n")
                    count_carac = 0
                    palavra = ""
                count_carac = 0

            
                    


                


