from analisador_lexico import lexico
import sys


#def main():

entrada = sys.argv[1:]
arquivo = './teste/' + entrada[0]

try:
    t = open(arquivo, 'r')
except:
    print("Erro ao abrir o arquivo")
file = lexico(t, entrada[0])
    #if __name__ == "__main__":
        #main()