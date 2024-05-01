# DataBase
import sqlite3
import Encrypt_Decrypt
# Extras
import logging

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
debug_DataBase = setup_logger('create database', 'logs/database.log')
debug_DataBase.info('---//---')


def Connect_to_DB():
    '''Returns a Connection and a Cursor SQL Objects'''
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as err:
        debug_DataBase.error(f'Err Opening DB: {err}')

def Ex_SQL_Code_Add_Data(code:str, values:tuple) -> bool:
    # Connect to databse:
    conn, cursor = Connect_to_DB()
    try:
        # execute and commit
        cursor.execute(code, values)
        conn.commit()
        # Close Connection and return True
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        # Return False and log Error
        debug_DataBase.error(f'\tError: {err}')
        # Close Connection and return False
        cursor.close()
        conn.close()
        return False

def Read_Full_Table(table:str) -> list[tuple]:
    '''
    Fetches data from table
    :param table: name of table
    :return: list[tuple] or None if fails
    '''
    # Connect to databse:
    conn, cursor = Connect_to_DB()

    # Fetch data!
    sql_code = f"SELECT * FROM {table}"
    try:
        cursor.execute(sql_code)
        table_data = cursor.fetchall()

        # Print and log data
        debug_DataBase.info('---')
        debug_DataBase.info(f"Listing all {table}:")
        print(f"\nTable {table}:")
        for entry in table_data:
            debug_DataBase.info(f'\t{entry}')
            print('\t', entry)
        # Close Connection
        cursor.close()
        conn.close()
        return table_data
    except Exception as err:
        debug_DataBase.error(f'\tError: {err}')
        # Close Connection
        cursor.close()
        conn.close()
        return None



# Create DataBase!
def CreateDB():
    # Connect:
    conn, cursor = Connect_to_DB()

    # Create DataBase:
    debug_DataBase.info('---')
    debug_DataBase.info("Creating DataBase:")
    sql_code = []

    # Utilizadores:
    sql_code.append('''CREATE TABLE utilizadores
    (id INTEGER PRIMARY KEY,
    utilizador TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    iv TEXT,
    activo INTEGER)''')

    # Colaboradores:
    sql_code.append('''CREATE TABLE colaboradores
    (id INTEGER PRIMARY KEY,
    num_colaborador INTEGER UNIQUE,
    nome TEXT NOT NULL,
    activo INTEGER)''')

    # Armários
    sql_code.append('''CREATE TABLE armarios
    (id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    local TEXT NOT NULL,
    activo INTEGER)''')

    # Items
    sql_code.append('''CREATE TABLE items
    (id INTEGER PRIMARY KEY,
    item TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    activo INTEGER)''')

    # Item Delivery
    sql_code.append('''CREATE TABLE entrega
        (id INTEGER PRIMARY KEY,
        data REAL,
        user_id INTEGER,
        colaborador_id INTEGER,
        item_id INTEGER,
        quantidade INTEGER,
        armario_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES utilizadores(id),
        FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id),
        FOREIGN KEY (item_id) REFERENCES items(id),
        FOREIGN KEY (armario_id) REFERENCES armarios(id))''')

    ok_counter = 0
    total_tried = 0
    for code in sql_code:
        total_tried += 1
        table = code.split()
        try:
            cursor.execute(code)
            conn.commit()
            debug_DataBase.info(f"\tTabela {table[2]} criada ok")
            ok_counter += 1
        except Exception as err:
            debug_DataBase.error(f'\tErr creating Table {table[2]}: {err}')

    # Close Connection
    cursor.close()
    conn.close()
    return ok_counter, total_tried


# Users:
def Add_User(username: str, password: str) -> bool:
    '''
    Inputs user into DataBase
    :param username:
    :param password:
    :return: True for 'All good' / False for error
    '''

    debug_DataBase.info('---')
    debug_DataBase.info("Inserting User into DataBase")
    debug_DataBase.info(f'\tUsername: {username}')

    # Validate User and Password:
    username.split()

    if len(username) < 3 or len(password) < 3:
        debug_DataBase.error("\tUsername / Password must have more then 5 character.")
        return False

    # Encrypt password
    iv, password_encryped = Encrypt_Decrypt.encriptar_dados(frase=password)
    sql_code = '''INSERT INTO utilizadores
    (utilizador, senha, iv, activo) values (?, ?, ?, ?)'''

    All_good = Ex_SQL_Code_Add_Data(sql_code, (username, password_encryped, iv, 1))
    if All_good:
        debug_DataBase.info("\tUser Added.")
        return True
    else:
        return False


def Validate_Login(user: str, password: str) -> bool:
    '''Login
    :return True all good
    :return False if user/password is wrong'''

    debug_DataBase.info('---')
    debug_DataBase.info("Validate Login")

    conn, cursor = Connect_to_DB()

    cursor.execute("SELECT * FROM utilizadores")
    users = cursor.fetchall()

    user_data = False
    for i in users:
        if i[1] == user:
            user_data = i
            break

    if not user_data:
        debug_DataBase.error("\tUsername not in DataBase!")
        return False

    User_Password = Encrypt_Decrypt.desencriptar_dados(iv=user_data[3], texto_encriptado=user_data[2])
    if password == User_Password:
        debug_DataBase.info(f"\tUser: {user} Loged in!")
        return True
    else:
        debug_DataBase.error("\tWrong Username or Password!")
        return False


# Workers
def Add_Worker(name: str, number: int = None) -> bool:
    '''
    Adding Worker to DB
    :param name:
    :param number:
    :return: True or False and logs why it failed
    '''
    debug_DataBase.info('---')
    debug_DataBase.info("Inserting Worker into DataBase")
    debug_DataBase.info(f'\tWorker name: {name}')

    # Validate name
    name.strip()

    if number == None:
        sql_code = '''INSERT INTO colaboradores
                    (nome, activo) values (?, ?)'''
        All_good = Ex_SQL_Code_Add_Data(sql_code, (name, 1))
    else:
        sql_code = '''INSERT INTO colaboradores
                        (num_colaborador, nome, activo) values (?, ?, ?)'''
        All_good = Ex_SQL_Code_Add_Data(sql_code, (number, name, 1))

    if All_good:
        debug_DataBase.info("\tEntry Added.")
        return True
    else:
        return False


# Storage
def Add_Storage(name:str, location:str):
    '''
        :param name:
        :param location:
        :return: True or False and logs why it failed
        '''

    debug_DataBase.info('---')
    debug_DataBase.info("Inserting Item into DataBase")
    debug_DataBase.info(f'\tStorage name: {name}')

    # Validate name
    name.strip()
    location.strip()
    '''if len(name) < 5:
        debug_DataBase.error("\tItem name to short")
        return False'''

    sql_code = '''INSERT INTO armarios
            (nome, local, activo) values (?, ?, ?)'''
    All_good = Ex_SQL_Code_Add_Data(sql_code, (name, location, 1))
    if All_good:
        debug_DataBase.info("\tEntry Added.")
        return True
    else:
        return False


# Items
def Add_Item(item_name:  str, description: str) -> bool:
    '''
    :param item_name:
    :param description:
    :return: True or False and logs why it failed
    '''

    debug_DataBase.info('---')
    debug_DataBase.info("Inserting Item into DataBase")
    debug_DataBase.info(f'\tItem name: {item_name}')

    # Validate name
    item_name.strip()
    if len(item_name) < 5:
        debug_DataBase.error("\tItem name to short")
        return False

    sql_code = '''INSERT INTO items
        (item, descricao, activo) values (?, ?, ?)'''
    All_good = Ex_SQL_Code_Add_Data(sql_code, (item_name, description, 1))
    if All_good:
        debug_DataBase.info("\tEntry Added.")
        return True
    else:
        return False


# Entries
def Deliver_Item(user_id: int, worker_id: int, item_id: int, num: int, storage_id: int) -> bool:
    '''

    :param user_id:
    :param worker_id:
    :param item_id:
    :param num:
    :param storage_id:
    :return: True or False and logs why it failed
    '''

    debug_DataBase.info('---')
    debug_DataBase.info("Deliver Item")
    debug_DataBase.info(f'\tItem name: ??')

    # get date and time

    #
    sql_code = '''INSERT INTO entrega
            (user_id, colaborador_id, item_id, quantidade, armario_id) values (?, ?, ?, ?, ?)'''
    All_good = Ex_SQL_Code_Add_Data(sql_code, (user_id, worker_id, item_id, num, storage_id))
    if All_good:
        debug_DataBase.info("\tEntry Added.")
        return True
    else:
        return False



if __name__ == '__main__':
    CreateDB()

    # Add test Users
    Add_User('Marco', '12345')
    Add_User('Polo', '54321')

    # Add test Colaboradores/workers
    Add_Worker('Marco', 12345)
    Add_Worker('Rita', 4596)

    # Add test Items
    Add_Item('Blue Pen', 'Normal Blue Pen')
    Add_Item('Red Pen', 'Normal Red Pen')
    Add_Item('Gloves S', 'Gloves size S')
    Add_Item('Gloves M', 'Gloves size M')
    Add_Item('Gloves L', 'Gloves size L')

    # Add test Storage
    Add_Storage('Warehouse', 'Main Warehouse')
    Add_Storage('Box 1', 'Work place 1')


    # Add Entries



    # Read Back All Data
    Read_Full_Table('utilizadores')
    Read_Full_Table('colaboradores')
    Read_Full_Table('armarios')
    Read_Full_Table('items')
    Read_Full_Table('entrega')