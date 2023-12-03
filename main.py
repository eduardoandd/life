import mysql.connector 
from mysql.connector import Error

tables_list= []

def criar_db(host,user,password,db_name):
    
    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database=db_name
        )
        
        print('Banco de dados já existe')
        #cursor = connection.cursor()
        #cursor.execute(f'DROP DATABASE {db_name}')
        
        return True
    
    except Error as err:
        print('Banco de dados não existe, criando banco de dados...')
        pass
    connection=connection=mysql.connector.connect( 
            host = host, 
            user = user, 
            password = password, 
        )
    cursor = connection.cursor()
    cursor.execute(f'CREATE DATABASE {db_name}')
    cursor.close()
    connection.close()
    print('Banco de dados criado com sucesso')
    
    return False

def conectar_db(host,user,password,db_name):
    
    try:
        connection = mysql.connector.connect(
            host = host,
            user=user,
            password = password,
            database = db_name
        )
        
        print('Conexão estabelicida com sucesso!')
        
        return connection
    
    except Error as err:
        print('Erro ao estabelecer conexão com o banco de dados: ', err)
        exit()
        

#================= CRUD =========================

def cria_tabela(host,user,password,db_name, table_name, id_name,dict):
    
    connection = conectar_db(host,user,password,db_name)
    cursor = connection.cursor()
    
    cursor.execute(f'CREATE TABLE {table_name} ({id_name} int auto_increment primary key)')
    
    for column,type_ in dict.items():
        
        cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {column} {type_}')
    
     


def main():
       
    criar_db('localhost','root','Edu10peixe@','life')
    
    while(True):
        
        dict ={}
        
        print('\n\n:::::: SELECIONE UMA OPÇÃO ::::::')
        print('1 - CRIAR UMA NOVA TABELA')
        print('1 - INSERIR DADOS EM UMA TABELA EXISTENTE')
        
        option = int(input('Digite a opção desejada: '))
        
        if option == 1:
            
            table_name = input('Digite o nome que você deseja dar para sua tabela: ')
            id_name = input('Digite como deseja chamar o seu identificador: ')
            
            tables_list.append(table_name)
            
            while (True):
                print('Insira as colunas com nome e tipo que deseja adicionar.')
                
                column = input('Insira o nome da coluna: ')
                type_ = input('Informe sua tipagem: ')
                
                opcao = int(input('Deseja continuar? [1]SIM, [2]NÃO'))
                
                dict[column] = type_
                
                if opcao == 1:
                    continue
                else:
                    break
                
            cria_tabela('localhost','root','Edu10peixe@','life', table_name, id_name,dict)
         
                
                
            
            
            
            
    

if __name__ == '__main__':
    main()