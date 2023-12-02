#Importando bibliotecas
import json
import os
from getpass import getpass

#--------------------------------------------------------------------------------------
#Função para receber pacotes de dados.

def cadastrarUsuariosEmLote(dados, **usuarios):
    usuarios_nao_inseridos = []

    for usuario_id, usuario_info in usuarios.items():
        cpf = usuario_info.get("CPF", "")
        nome = usuario_info.get("Nome", "")

        cpfValido = validarCPF(cpf)
        if cpfValido is False:
            print(f"Usuário ID: {usuario_id}, CPF {cpf} inválido. Não foi inserido.")
            usuarios_nao_inseridos.append(usuario_id)
            continue
        elif cpfValido is True:
            cpfValido = cpf

        nomeValido = validaLetrasEspacos(nome)
        if nomeValido is False:
            print(f"Usuário ID: {usuario_id}, nome {nome} inválido. Não foi inserido.")
            usuarios_nao_inseridos.append(usuario_id)
            continue
        elif nomeValido is True:
            nomeValido = nome

        telefoneValido = usuario_info.get("Telefone", "")
        enderecoValido = usuario_info.get("Endereço", "")

        # Verifica se o CPF ou nome já existem em dataGeral
        #if any(item["CPF"] == cpfValido or item["Nome"] == nomeValido for item in dados.values()):
        if any(item["CPF"] == cpfValido for item in dados.values()):
            print(f"Usuário ID: {usuario_id}, com CPF {cpfValido} ou nome {nomeValido} já existe em dataGeral. Não foi inserido.")
            continue

        # Verifica se o CPF ou nome já existem em usuarios_nao_inseridos
        if any(usuario_info == usuarios[user_id] for user_id in usuarios_nao_inseridos):
            print(f"Usuário ID: {usuario_id}, com CPF {cpfValido} ou nome {nomeValido} já está marcado como não inserido. Não foi inserido.")
            continue

        # Cria o novo usuário com os valores corretos
        novoUsuario = {
            "Status": True,
            "CPF": cpfValido,
            "Nome": nomeValido,
            "Telefone": telefoneValido if telefoneValido is not False else None,
            "Endereço": enderecoValido if enderecoValido is not False else None
        }

        dados = addID(dados, novoUsuario)

    return dados


#---------------------------------------------------------------------------------------
#Função para carregar o arquivo json
'''Armazena as informações do arquivo json na varável dataGeral
E retorna dataGeral'''

def carregarArquivo(nomeArquivo):
    if os.path.exists(nomeArquivo):
        with open(nomeArquivo, 'r', encoding='utf-8') as arquivo:
            dataGeral = json.load(arquivo)
        return dataGeral
    else:
        return {}

#---------------------------------------------------------------------------------------
#Função para salvar o arquivo json
def salvarArquivo(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=2)

#---------------------------------------------------------------------------------------
#Adicionar usuário
'''Função que insere o novo usuário no arquivo de dados
Utiliza o tamanho do dicionário para criar o ID'''

def addID(dados,usuario): # mudar para addID
    dados[len(dados)+1] = usuario
    return(dados)

#---------------------------------------------------------------------------------------
#Excluir usuário
'''Tem como entrada o arquivo de dados e uma lista de IDs
E altera o Status para False caso encontre o ID no aqruivo de dados'''

def excluirUsuario(dados, *ids):
    for id in ids:
        if id in dados:
            print(f"Cadastro de {dados[str(id)]['Nome']} foi excluído.")
            dados[str(id)]["Status"] = False
        else:
            print("Usuário não encontrado")
    return dados

#---------------------------------------------------------------------------------------
#Editar informação de um usuário
'''Percorre a lista de IDs, quando o ID é encontrado solicita
quais informações deseja alterar. Caso digite um opção inválida
o programa retorna um erro e não altera as informações'''

def editUsuario(dados, *ids):
    for id in ids:
        if (id in dados) and (dados[id]["Status"] == True):
            print(f"ID {id} - Usuário encontrado")
            opcao = int(input("Qual informação deseja alterar: 1-Nome 2-Telefone 3-Endereço: "))
            if opcao == 1:
                nome = input("Insira o nome: ")
                dados[id]["Nome"] = validaInput(nome,validaLetrasEspacos)
            elif opcao == 2:
                telefone = input("Número do celular com DDD: ")
                telefoneValidado = validaInput(telefone, validaTelefone)
                dados[id]["Telefone"] = numCelular(telefoneValidado)
                if dados[id]["Telefone"] == "":
                    dados[id]["Telefone"] = "Não informado"
            elif opcao == 3:
                endereco = input("Insira o endereço: ")
                dados[id]["Endereço"] = validaInput(endereco,validaEndereco)
                if dados[id]["Endereço"] == "":
                    dados[id]["Endereço"] = "Não informado"
            else:
                print("ERRO. Informações não alteradas")
        else:
            print(f"Usuario com id {id} não encontrado.\n")
    return(dados)

#---------------------------------------------------------------------------------------
#Exibir informações de um usuário
'''Percorre o arquivo de dados, mostrando as informações de cada
ID solicitado.'''

def exibirUsuarios(dados,*ids):
    for id in ids:
        if id in dados and dados[id]["Status"] == True:
            print(f'CPF: {dados[id]["CPF"]}')
            print(f'Nome: {dados[id]["Nome"]}')
            print(f'Telefone: {dados[id]["Telefone"]}')
            print(f'Endereço: {dados[id]["Endereço"]}\n')
        else:
            print(f"ID {id} - Usuário não encontrado\n")

#---------------------------------------------------------------------------------------
#Exibe todas as informações dos usuários
'''Percorre o arquivo de dados, mostrando as informações de todos os
IDs que estão com status True.'''

def exibirTodosUsuarios(dados):
    for key,values in dados.items():
        if dados[key]["Status"] == True:
            print(f'ID: {key}')
            print(f'CPF: {dados[key]["CPF"]}')
            print(f'Nome: {dados[key]["Nome"]}')
            print(f'Telefone: {dados[key]["Telefone"]}')
            print(f'Endereço: {dados[key]["Endereço"]}\n')

#---------------------------------------------------------------------------------------
#Função que solicita os dados para o usuário
def solicitaDados(dados):

    print("Digite as informações do usuário")
    cpf = input("CPF: ")
    cpfNumeros = ''.join([char for char in cpf if char.isdigit()])
    cpfValido = validaInput(cpfNumeros, validarCPF)

#CPF e Nome são campos obrigatórios
#Faz uma busca para saber se a pessoa já existe na base dados
#Caso exista mas o Status esteja igual a False, pergunta se quer ativar o cadastro
#Se a opção for ativar, pergunta se quer atualizar informações
#Caso o Status esteja True, pergunta se quer atualizar informações
    id = buscaUsuario(dados,cpfValido)
    usuario = {}
    if id != False:
        print("Usuário existente")
        if dados[id]["Status"] == False:
            resposta = input("Está desabilitado, deseja alterar? (S/N):")
            if resposta in "Ss":
                dados[id]["Status"] = True
                resposta = input("Deseja atualizar dados? (S/N):")
                if resposta in "Ss":
                    dadosEdt = editUsuario(dados,id)
                    return dadosEdt
                else:
                    return dados
        else:
            resposta = input("Deseja atualizar dados? (S/N):")
            if resposta in "Ss":
                dadosEdt = editUsuario(dados,id)
                return dadosEdt
            else:
                return dados
#Se o usuário não existir, pergunta as informações necessárias para completar o cadastro
    else:
        usuario["Status"] = True
        usuario["CPF"] = cpfValido
        nome = input("Nome: ")
        usuario["Nome"] = validaInput(nome, validaLetrasEspacos)
        #usuario["Telefone"] = numCelular()
        telefone = input("Número do celular com DDD: ")
        telefoneValidado = validaInput(telefone, validaTelefone)
        usuario["Telefone"] = numCelular(telefoneValidado)
        if usuario["Telefone"] == "":
            usuario["Telefone"] = "Não informado"
        endereco = input("Endereço: ").title()
        usuario["Endereço"] = validaInput(endereco, validaEndereco)
        if usuario["Endereço"] == "":
            usuario["Endereço"] = "Não informado"

        dadosEdt = addID(dados, usuario)
        return dadosEdt

#---------------------------------------------------------------------------------------
#Função para criar a lista de IDs
'''Dependendo a opção que o usuário escolher, é necessário informar os IDs que
deseja obter a informação'''

def solicitaIDs():
    lista = []

    # Loop principal
    while True:
        # Pergunta ao usuário se ele deseja adicionar um número à lista
        resposta = input("Deseja adicionar um ID? (S/N): ")

        # Tenta converter a resposta em um caractere
        try:
            resposta = resposta[0].upper()

        # Se a conversão falhar, trata a exceção
        except IndexError:
            # Imprime uma mensagem de erro
            print("Resposta inválida.")
            continue

        # Se a resposta for S
        if resposta == "S":
            # Tenta converter a resposta em um número inteiro
            try:
                id = int(input("Qual ID você deseja adicionar? "))

            # Se a conversão falhar, trata a exceção
            except ValueError:
                # Imprime uma mensagem de erro
                print("Resposta inválida.")
                continue

            # Adiciona o número à lista
            lista.append(str(id))

        # Se a resposta for N
        elif resposta == "N":
            # Termina o loop
            break
    return lista
#---------------------------------------------------------------------------------------
#Função responsável por fazer a busca do nome na base de dados
#Retorna o valor do ID caso encontre

def buscaUsuario(dados,cpfValido):
    for id in dados:
        if cpfValido == dados[id]["CPF"]:
            busca = id
            break
        else:
            busca = False
    return busca

#Função para validar número de telefone
#Se não colocar um valor, é adicionado no cadastro Não Informado
#Caso digite menos ou mais do que 11 digitos, programa pede para digitar novamente

#---------------------------------------------------------------------------------------
def numCelular(numeroCelular):
    #print("Digite o número do telefone, caso não queira informar, deixar em branco.")
    while True:
        #numeroCelular = input('Telefone Celular com DDD: ' )
        try:
            if len(numeroCelular) != 11:
                raise ValueError
            else:
                numeroCelular = int(numeroCelular)# se contiver letras causa um ValueError
                numeroCelular = str(numeroCelular)
                celular = numeroCelular
                telFormatado = '({}) {}-{}-{}'.format(celular[0:2],
                                    celular[2] ,celular[3:7], celular[7:])
                break

        except ValueError:
            if len(numeroCelular) == 0:
                #print('Você não inofrmou um número')
                telFormatado = ""
                break
            else:
                print('Número inválido, o número precisa ter 11 números inteiros')

    return telFormatado

#---------------------------------------------------------------------------------------
# Função que valida input no geral.

def validaInput(valor, funcaoValidadora, msg = 'Digite novamente: '):
    while not funcaoValidadora(valor):
        print(f'Informação "{valor}" inválida!')
        valor = input(msg)

    confirmacao = input(f'Confirme a informação "{valor}"\nDigite 1 para confirmar, 2 para modificar: ')
    while confirmacao not in ['1', '2']:
        confirmacao = input('Opção inválida. Digite 1 para confirmar, 2 para modificar: ')

    if confirmacao == '2':
        valor = input('Digite um novo valor: ')
        valor = validaInput(valor, funcaoValidadora)

    return valor

#---------------------------------------------------------------------------------------
# Funções Validadoras

# Função validadora Nome
def validaLetrasEspacos(string):
    return all(caracter.isalpha() or caracter.isspace() for caracter in string)

# Função validadora telefone
def validaTelefone(string):
    strNum = lambda string: ''.join(char for char in string if char.isdigit())
    numeroLimpo = strNum(string)

    if len(numeroLimpo) == 11 or len(numeroLimpo) == 0:
        return True
    else:
        return False

    #return numeroLimpo if len(numeroLimpo) == 11 or len(numeroLimpo) == 0 else False

# Função validadora Endereço.
def validaEndereco(endereco):
    if len(endereco) > 100:
        return False

    return True

# Função Validadora CPF

def validarCPF(string):
    digitosValidos = ''.join([char for char in string if char.isdigit()])

    if len(digitosValidos) != 11:
        return False

    else:
        nove_digitos = digitosValidos[:9]
        contador_regressivo_1 = 10


        resultado_digito_1 = 0
        for digito in nove_digitos:
            resultado_digito_1 += int(digito) * contador_regressivo_1
            contador_regressivo_1 -= 1
        digito_1 = ((resultado_digito_1 * 10) % 11)
        digito_1 = digito_1 if digito_1 <= 9 else 0

        dez_digitos = digitosValidos[:9] + str(digito_1)
        contador_regressivo_2 = 11

        resultado_digito_2 = 0
        for digito in dez_digitos:
            resultado_digito_2 += (int(digito) * contador_regressivo_2)
            contador_regressivo_2 -= 1
        digito_2 = ((resultado_digito_2 * 10) % 11)
        digito_2 = digito_2 if digito_2 <= 9 else 0

        CPFValidado = f'{nove_digitos}{digito_1}{digito_2}'

        if digitosValidos == CPFValidado:
            return CPFValidado
        else:
            return False

#---------------------------------------------------------------------------------------
def solicitaArquivo():
    # Solicita o nome do arquivo ao usuário
    while True:
        nomeArquivo = input("Digite o nome do arquivo ou sair para fechar o programa: ")

        # Tenta abrir o arquivo
        try:
            with open(nomeArquivo, "r") as arquivo:
                # O arquivo existe
                return nomeArquivo

        # Se o arquivo não existir, trata a exceção
        except FileNotFoundError:
            # Imprime uma mensagem de erro
            if nomeArquivo != "sair":
                print(f"O arquivo {nomeArquivo} não existe.")

        # Se o usuário digitar "sair", sai do programa
        if nomeArquivo == "sair":
            return None
#---------------------------------------------------------------------------------------
#Carrega as informações do arquivo Json na variável dataGeral
#Caso o nome do arquivo seja diferente, aterar a variável nomeArquivo

def main():
    nomeArquivo = solicitaArquivo()
    if nomeArquivo == None:
        print('Até mais')
    else:
        dataGeral = carregarArquivo(nomeArquivo)

        while True:
            print("Boas vindas ao nosso sistema:")
            print("-"*30)
            print("1 - Inserir usuário")
            print("2 - Excluir usuário")
            print("3 - Atualizar usuário")
            print("4 - Informações de um usuário")
            print("5 - Informações de todos os usuários")
            print("6 - Sair")
            print("-"*30)

            while True:
                opcao = int(input("Digite uma opção: "))
                if opcao not in range(1,7):
                    print("Opção inválida. Tente novamente")
                else:
                    break
            if opcao == 1:
                umOuMais = input('Deseja inserir um usuário ou varios?\n1- para um usuário \n2- para vários:\n0- para sair:\n ')
                while umOuMais not in ('1','2','0'):
                    print('Opção inválida')
                    umOuMais = input('Deseja inserir um usuário ou varios?\n1- para um usuário \n2- para vários:\n0- para sair:\n ')

                if umOuMais == '1':
                    dataGeral = solicitaDados(dataGeral)
                elif umOuMais == '2':
                    loteUsuariosJSON = solicitaArquivo()
                    if loteUsuariosJSON != None:
                        loteUsuarios = carregarArquivo(loteUsuariosJSON)
                        dataGeral = cadastrarUsuariosEmLote(dataGeral, **loteUsuarios)
                    else:
                        continue
                else:
                    continue
            elif opcao == 2:
                ids = solicitaIDs()
                dataGeral = excluirUsuario(dataGeral,*ids)
            elif opcao == 3:
                ids = solicitaIDs()
                dataGeral = editUsuario(dataGeral,*ids)
            elif opcao == 4:
                ids = solicitaIDs()
                exibirUsuarios(dataGeral,*ids)
            elif opcao == 5:
                senha = getpass("Digite a senha: ")
                if senha == "12345":
                    exibirTodosUsuarios(dataGeral)
                else:
                    print("Senha inválida")
            else:
                break
            salvarArquivo(nomeArquivo, dataGeral)
            dataGeral = carregarArquivo(nomeArquivo)

# Chamando a main() para iniciar o programa.
main()