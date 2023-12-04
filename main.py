import mysql.connector 
from mysql.connector import Error

tables_list= []


#================= AUX =========================

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
        
def show_tables(conn):
    
    # host='localhost'
    # user='root'
    # password='Edu10peixe@'
    # db_name='life'
    
    connection = conn
    cursor = connection.cursor()
    tables ='SHOW TABLES'
    cursor.execute(tables)
    results = cursor.fetchall()
    print(results)
     
    return results


#================= CRUD =========================

def cria_tabela(host,user,password,db_name,conn,table_name, id_name,dict):
    
    connection = conn
    cursor = connection.cursor()
    
    cursor.execute(f'CREATE TABLE {table_name} ({id_name} int auto_increment primary key)')
    
    for column,type_ in dict.items():
        
        cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {column} {type_}')
        
def insert_table(table_name,values,name_columns_list, conn):
    
    connection = conn 
    cursor = connection.cursor() 
       
    sql = f"INSERT INTO {table_name} ({', '.join(name_columns_list)}) VALUES ({', '.join(['%s' for _ in values])})"

    

    cursor.execute(sql, values) 
    connection.commit() 

    cursor.close() 
    connection.close() 
       

       
   
   
   
   
   
   



#================= PRINCIPAL =========================

def main():
    
    host='localhost'
    user='root'
    password='Edu10peixe@'
    db_name='life'
    
    criar_db(host,user,password,db_name)
    
    conn = conectar_db(host,user,password,db_name)
    
    while(True):
        
        dict ={}
        
        print('\n\n:::::: SELECIONE UMA OPÇÃO ::::::')
        print('1 - CRIAR UMA NOVA TABELA')
        print('2 - INSERIR DADOS EM UMA TABELA EXISTENTE')
        
        option = int(input('Digite a opção desejada: '))
        
        if option == 1:
            
            table_name = input('Digite o nome que você deseja dar para sua tabela: ')
            id_name = input('Digite como deseja chamar o seu identificador: ')
            
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
                
            cria_tabela(host,user,password,db_name, conn, table_name, id_name,dict)
            
        elif option ==2:
            
            print('\n\n:::::: LISTA DE TABELAS ::::::')
            
            conn_ = conectar_db(host,user,password,db_name)
            
            tables=show_tables(conn_)
            
            insert_option=input('Qual tabela você deseja alterar? (ESCREVA O NOME): ')
            
            if insert_option in  [table[0] for table in tables]:
                
                table_columns =  f'DESC {insert_option};'
                
                cursor = conn.cursor()
                cursor.execute(table_columns)
                columns = cursor.fetchall()
   
                name_columns = [column for column in columns]
   
                values = []
                name_columns_list = []
                
                for value in columns[1:]:
                    
                    column_value = input(f'Insira um valor para coluna {value[0]}: ')
                    name_columns_list.append(value[0])
                    values.append(column_value)
                    
                
                insert_table(insert_option,values,name_columns_list,conn)
                
         
                
                
            
            
            
            
    

if __name__ == '__main__':
    main()