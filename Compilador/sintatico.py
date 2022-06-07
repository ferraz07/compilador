
def sintatico(vetorTokens):
    file = './saidas/'+ '_saida_sintatico.txt'
    saida = open(file, 'w')
    global vetTokens
    global posicao
    posicao = 0
    vetTokens = []
    cont = 0
    while cont < len(vetorTokens):
        vetTokens.insert(cont, vetorTokens[cont])
        cont +=1
    token = 0
    i = 0
    while i < len(vetTokens):   
        if vetTokens[posicao] == 2:
            validadeDec = verificarDec(vetTokens[posicao+1], posicao+1)
            if validadeDec == True:
                saida.write("DECLARACAO \n")
                posicao = posicao + 2
                i = i+2
            else:
                validadeFunc = verificarFuncao(vetTokens[posicao+1], posicao+1)
                if validadeFunc == True:
                    saida.write("FUNCAO  \n")
                    posicao = posicao + 4
                    i=i+4
                else:
                    print("ERRO SINTATICO - Funcao\n")
                #posicao = posicao - 1
        elif vetTokens[posicao] == 3:
            validadeAtt = verificarAtt(vetTokens[posicao+1], posicao+1)
            if validadeAtt == True:
                saida.write("ATRIBUICAO \n")
                posicao = posicao + 2
                i = i+2
            else:
                print("ERRO SINTATICO - atribuicao")
        elif vetTokens[posicao] == 8:
            validadeFor = verificarFor(vetTokens[posicao+1], posicao+1)
            if validadeFor == True:
                saida.write("FOR \n")
                posicao = posicao + 12
                i = i+12
            else:
                print("ERRO SINTATICO - For")
        elif vetTokens[posicao] == 9:
            validadeWhile = verificarWhile(vetTokens[posicao+1], posicao+1)
            if validadeWhile == True:
                saida.write("WHILE \n")
                posicao = posicao + 5
                i = i + 5
            else:
                print("ERRO SINTATICO - While")
        elif vetTokens[posicao] == 7:
            validadeIf = verificarIf(vetTokens[posicao+1], posicao+1)
            if validadeIf == True:
                saida.write("IF  \n")
                posicao = posicao + 5
                i = i +5
            else:
                print("ERRO SINTATICO - If\n")
        elif vetTokens[posicao] == 17:
            validadeElse = verificarElse(vetTokens[posicao+1], posicao+1)
            if validadeElse == True:
                saida.write("ELSE \n")
                posicao = posicao + 2
                i = i +2
            else:
                print("ERRO SINTATICO- Else\n")          
        posicao += 1
        i+=1
        if i == len(vetTokens):
            break


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
