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

def get_columns(table_selected,tables,conn):
    
    if table_selected in  [table[0] for table in tables]:
                
                table_columns =  f'DESC {table_selected};'
                
                cursor = conn.cursor()
                cursor.execute(table_columns)
                columns = cursor.fetchall()

    return columns



#================= CRUD =========================

def cria_tabela(conn,table_name, id_name,dict):
    
    connection = conn
    cursor = connection.cursor()
    
    cursor.execute(f'CREATE TABLE {table_name} ({id_name} int auto_increment primary key)')
    
    for column,type_ in dict.items():
        
        cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {column} {type_}')
        
    cursor.close()
    connection.close()

def select_tabela(table_name,conn):
    cursor  = conn.cursor()
    
    sql = f'SELECT * FROM {table_name}'
    
    cursor.execute(sql) 
    results = cursor.fetchall()
    
    print(results) 
    cursor.close() 
    conn.close()
    
    return results 
        
def insert_table(table_name,values,name_columns_list, conn):
    
    connection = conn 
    cursor = connection.cursor() 
       
    sql = f"INSERT INTO {table_name} ({', '.join(name_columns_list)}) VALUES ({', '.join(['%s' for _ in values])})"

    cursor.execute(sql, values) 
    connection.commit() 

    cursor.close() 
    connection.close() 
       
def update_table(table_name,column_name,new_value,id_value,id,conn):
     
    cursor = conn.cursor()

    sql = f'UPDATE {table_name} SET {column_name}=%s WHERE {id} = {id_value}'
    data = (new_value,)  

    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

def deleta_table(table_name,id,id_value,conn):
    
    cursor = conn.cursor()
    sql = f'DELETE FROM {table_name} WHERE {id} = %s'
    data = (id_value,)
    cursor.execute(sql,data)
    conn.commit()
    cursor.close()
    conn.close()
    
    
    
#================= PRINCIPAL =========================

def main():
    
    host='localhost'
    user='root'
    password='Edu10peixe@'
    db_name='life'
    
    criar_db(host,user,password,db_name)
    
    while(True):
        
        conn = conectar_db(host,user,password,db_name)
        
        dict ={}
        
        print('\n\n:::::: SELECIONE UMA OPÇÃO ::::::')
        print('1 - CRIAR UMA NOVA TABELA')
        print('2 - INSERIR DADOS EM UMA TABELA EXISTENTE')
        print('3 - ATUALIZAR DADOS EM UMA TABELA EXISTENTE')
        print('4 - DELETAR DADOS EM UMA TABELA EXISTENTE')
        print('5 - VISUALIZAR DADOS EM UMA TABELA EXISTENTE')
        
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
            
            tables=show_tables(conn)
            
            insert_option=input('Qual tabela você deseja alterar? (ESCREVA O NOME): ')
            
            columns = get_columns(insert_option,tables,conn)
   
            values = []
            name_columns_list = []
            
            for value in columns[1:]:
                
                column_value = input(f'Insira um valor para coluna {value[0]}: ')
                name_columns_list.append(value[0])
                values.append(column_value)
                
            insert_table(insert_option,values,name_columns_list,conn)

        elif option ==3:
            
            while(True):
                
                option=int(input('Deseja fazer alguma atualização [1]SIM [2]NÃO'))
                
                if option ==1:
            
                    print('\n\n:::::: LISTA DE TABELAS ::::::')

                    tables=show_tables(conn)

                    update_option=input('Qual tabela você deseja alterar? (ESCREVA O NOME): ')

                    columns = get_columns(update_option,tables,conn)

                    id = columns[0][0]

                    print([column[0] for column in columns])

                    column_name=input('Informe qual coluna deseja alterar: ')

                    print(select_tabela(update_option,conn))
                    id_value=int(input('Informe o id da coluna: '))
                    new_value = input('Informe o novo valor: ')

                    conn = conectar_db(host,user,password,db_name)
                    update_table(update_option,column_name,new_value,id_value,id,conn)
            
                elif option==2:
                    break
        
        elif option ==4:
            print('\n\n:::::: LISTA DE TABELAS ::::::')

            tables=show_tables(conn)

            delete_option=input('Qual tabela você deseja alterar? (ESCREVA O NOME): ')

            columns = get_columns(delete_option,tables,conn)
            
            id = columns[0][0]
            
            id_value = int(input('Informe o id que deseja remover: '))
            
            conn = conectar_db(host,user,password,db_name)
            
            deleta_table(delete_option,id,id_value,conn)
                    
        elif option ==5:
            
            tables=show_tables(conn)

            select_option=input('Qual tabela você deseja VISUALIZAR? (ESCREVA O NOME): ')
            
            conn = conectar_db(host,user,password,db_name)
            select_tabela(select_option,conn)        
            
            
            
         
                
                
            
            
            
            
    

if __name__ == '__main__':
    main()