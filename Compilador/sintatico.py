# na tabelaVerificar temos que 1 representa que foi declarado, 2 representada que foi incializado, 3 representa que o ID é uma funcao.

def sintatico(iden, vetorTokens, vetorIDs):
    file = './saidas/'+ iden + '_saida_sintatico.txt'
    saida = open(file, 'w')
    geracao_codigo = './saidas/'+ iden + '_saida_geracao_codigo.txt'
    geracao_cod = open(geracao_codigo, 'w')
    global vetTokens
    global posicao
    posicao = 0
    vetTokens = []
    tabelaAtt = []
    tabelaVerificar = []
    cont = 0
    while cont < len(vetorTokens):
        vetTokens.insert(cont, vetorTokens[cont])
        cont +=1
    i = 0
    numero = 0
    contadorId = 0
    contadorTabela = 0
    while i < len(vetTokens):   
        if vetTokens[posicao] == 2:
            validadeDec = verificarDec(vetTokens[posicao+1], posicao+1)
            if validadeDec == True:
                if vetorIDs[contadorTabela] in tabelaAtt:
                    print(f"Variavel com esse nome ja declarada: {vetorIDs[contadorId]}\n")
                else:
                    tabelaAtt.insert(contadorTabela, vetorIDs[contadorTabela])
                    tabelaVerificar.insert(contadorTabela, 1)
                saida.write("DECLARACAO \n")
                geracao_cod.write(f"var{numero}:  .word\n")
                contadorTabela = contadorTabela + 1
                contadorId = contadorId + 1
                numero = numero + 1
                posicao = posicao + 2
                i = i+2
            else:
                validadeFunc = verificarFuncao(vetTokens[posicao+1], posicao+1)
                if validadeFunc == True:
                    saida.write("FUNCAO  \n")
                    geracao_cod.write(f"/*label*/\n{vetorIDs[contadorId]}: \n")
                    tabelaAtt.insert(contadorTabela, vetorIDs[contadorTabela])
                    tabelaVerificar.insert(contadorId, 3)
                    contadorTabela = contadorTabela + 1
                    contadorId = contadorId + 1
                    posicao = posicao + 4
                    i=i+4
                else:
                    print("ERRO SINTATICO - Funcao\n")
        elif vetTokens[posicao] == 3:
            validadeAtt = verificarAtt(vetTokens[posicao+1], posicao+1)
            if validadeAtt == True:
                saida.write("ATRIBUICAO \n")
                geracao_cod.write(f"li $s{numero}, {numero+2}\n")
                tabelaVerificar.insert(contadorId, 2)
                contadorId = contadorId + 1
                contadorTabela = contadorTabela + 1
                numero = numero + 1
                posicao = posicao + 2
                i = i+2
            else:
                print("ERRO SINTATICO - atribuicao")
        elif vetTokens[posicao] == 8:
            validadeFor = verificarFor(vetTokens[posicao+1], posicao+1)
            if validadeFor == True:
                contadorTabela = contadorTabela + 3
                contadorId = contadorId + 3
                saida.write("FOR \n")
                geracao_cod.write(
                    f"move $s0, $zero\n/*label*/\nFOR:\nslt $t0, $s0 ,$s{numero}\nbeq $t0, $zero, EXIT\naddi $s0, $s0, 1\nj FOR\n\nEXIT\n")
                posicao = posicao + 12
                i = i+12
            else:
                print("ERRO SINTATICO - For")
        elif vetTokens[posicao] == 9:
            validadeWhile = verificarWhile(vetTokens[posicao+1], posicao+1)
            if validadeWhile == True:
                saida.write("WHILE \n")
                geracao_cod.write(f"/*label*/\nWHILE: \nbne $t{numero}, $s{numero}, EXIT\nj WHILE\n")
                contadorTabela = contadorTabela + 1
                numero = numero + 1
                posicao = posicao + 5
                i = i + 5
            else:
                print("ERRO SINTATICO - While")
        elif vetTokens[posicao] == 7:
            validadeIf = verificarIf(vetTokens[posicao+1], posicao+1)
            if validadeIf == True:
                saida.write("IF  \n")
                geracao_cod.write(f"BNE $r{numero},$r{numero+1}, Else\n")
                contadorTabela = contadorTabela + 1
                numero = numero + 1
                posicao = posicao + 5
                i = i +5
            else:
                print("ERRO SINTATICO - If\n")
        elif vetTokens[posicao] == 17:
            validadeElse = verificarElse(vetTokens[posicao+1], posicao+1)
            if validadeElse == True:
                saida.write("ELSE \n")
                geracao_cod.write("/*label*/\nElse: \n")
                posicao = posicao + 2
                i = i +2
            else:
                print("ERRO SINTATICO- Else\n")          
        posicao += 1
        i+=1
        if i == len(vetTokens):
            break
    for i in range(len(vetorIDs)):
        if vetorIDs[i] not in tabelaAtt:
            print(f"Variavel nao declarada: {vetorIDs[i]}\n")
    

def verificarDec(token, posicao):
    if token == 3:    
        return verificarDec(vetTokens[posicao+1], posicao+1)
    elif token == 15:
        posicao = posicao + 2
        return True
    else:
        return -1


def verificarAtt(token, posicao):
    aux = False
    if token == 5:
        verificarAtt(vetTokens[posicao+1], posicao+1)
        return True
    elif token == 1 or token == 3:
        aux = verificarAtt(vetTokens[posicao+2], posicao+2)
        return True 
    elif token == 15:
        return True
    else:
        return -1


def verificarFor(token, posicao): 
    passou = 0
    if token == 11:
        verificarFor(vetTokens[posicao+1], posicao+1)
        return True
    validadeLoop1 = verificarDec(vetTokens[posicao+1], posicao +1)
    if validadeLoop1 == True:
        verificarFor(vetTokens[posicao+4], posicao +4)
        return True
    elif token == 15:
        verificarFor(vetTokens[posicao+5], posicao+5)
        return True
    validadeLoop2 = verificarAtt(vetTokens[posicao+6], posicao +6)
    if validadeLoop2 == True:
        verificarFor(vetTokens[posicao+8], posicao + 8)
        return True
    elif token == 3:
        verificarFor(vetTokens[posicao+10], posicao+10)
        return True
    elif token == 5:
        if passou == 0:
            passou = 1
            verificarFor(vetTokens[posicao+11], posicao+11)
            return True
        else:
            pass
    elif token == 5:
        verificarFor(vetTokens[posicao+12], posicao+12)
        return True
    elif token == 12:
        return True


def verificarWhile(token, posicao):
    if token == 11:
        verificarWhile(vetTokens[posicao+1], posicao+1)
        return True
    elif token == 3:
        verificarWhile(vetTokens[posicao+2], posicao+2)
        return True
    elif token == 6:
        verificarWhile(vetTokens[posicao+3], posicao+3)
        return True
    elif token == 1 or token == 3:
        verificarWhile(vetTokens[posicao+4], posicao+4)
        return True
    elif token == 12:
        return True

def verificarFuncao(token, posicao):
    if token == 3:
        return verificarFuncao(vetTokens[posicao+1], posicao+1)
    elif token == 11:
        return verificarFuncao(vetTokens[posicao+2], posicao+2)
    elif token == 12:
        return verificarFuncao(vetTokens[posicao+3], posicao+3)
    elif token == 13:
        return True 
    else:
        return False
    
    

def verificarIf(token, posicao):
    if token == 11:
        verificarIf(vetTokens[posicao+1], posicao+1)
        return True
    elif token == 3:
        verificarIf(vetTokens[posicao+2], posicao +2)
        return True
    elif token == 6:
        verificarIf(vetTokens[posicao+3], posicao+3)
        return True
    elif token == 1 or token == 3:
        verificarIf(vetTokens[posicao+4], posicao+4)
        return True
    elif token == 12:
        return True
    

def verificarElse(token, posicao):
    if token == 13:
        verificarElse(vetTokens[posicao+1], posicao+1)
        return True
