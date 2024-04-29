import sqlite3
import logging
import os
import Encript_Decript


# globals
DB_FILE = 'DataBase/database.db'


# Setup logging:
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Debug DB Read/Write/Delete
debug_DataBase = setup_logger('creat database', 'logs/database.log')


def Connect_to_DB():
    '''Returns a Connection and a Cursor SQL Objects'''
    conn, cursor = None, None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as err:
        debug_DataBase.error(f'Err Opening DB: {err}')


# Create / Delete
def CreateDB():
    # Connect:
    conn, cursor = Connect_to_DB()

    # Create DataBase:
    debug_DataBase.info("Creating DataBase:")
    sql_code = []
    # Utilizadores:
    sql_code.append('''CREATE TABLE IF NOT EXISTS utilizadores
    (id INTEGER PRIMARY KEY,
    utilizador TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    iv TEXT,
    activo INTEGER)''')
    
    # Colaboradores:
    sql_code.append('''CREATE TABLE IF NOT EXISTS colaboradores
    (id INTEGER PRIMARY KEY,
    num_colaborador INTEGER UNIQUE,
    nome TEXT NOT NULL,
    activo INTEGER)''')

    # Armários
    sql_code.append('''CREATE TABLE IF NOT EXISTS armarios
    (id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    local TEXT NOT NULL,
    activo INTEGER)''')

    # Items
    sql_code.append('''CREATE TABLE IF NOT EXISTS items
    (id INTEGER PRIMARY KEY,
    item TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    activo INTEGER)''')

    for code in sql_code:
        try:
            table = code.split()
            cursor.execute(code)
            conn.commit()
            debug_DataBase.info(f"\tTabela {table[5]} criada ok")
        except Exception as err:
            debug_DataBase.error(f'\tErr creating Table {table[5]}: {err}')

    # Close Connection
    cursor.close()
    conn.close()

def NukeDB():
    '''DELETE & Rebuild DabaBase'''
    if os.path.exists(DB_FILE):
        os.remove('DataBase/database.db')
        print("Nuked!")


def Validate_Login(self, user:str, password:str) -> bool:
    '''Login'''
    conn, cursor = Connect_to_DB()

    cursor.execute("SELECT * FROM utilizadores")
    users = cursor.fetchall()

    user_data = False
    for i in users:
        if i[1] == user:
            #print("\tUser Found!")
            user_data = i
            break
    
    User_Password = Encript_Decript.desencriptar_dados(iv=user_data[3], texto_encriptado=user_data[2])
    if password == User_Password:
        #print('\tLogin OK')
        return True
    else:
        #print("\tWrong Username or Password")
        Popup(1, 'Wrong Username or Password')
        return False



if __name__ == '__main__':
    CreateDB()
    #NukeDB()

