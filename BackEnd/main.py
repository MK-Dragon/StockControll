import sqlite3
import logging
import os


# globals
DB_FILE = 'DataBase/database.db'


# Setup logging

def setup_logger(self, name, log_file, level=logging.INFO):
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



def CreateDB():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        '''cursor.execute()'''
        debug_DataBase.info("DataBase Created")
    except Exception as err:
        debug_DataBase.error(f'Err creating DB: {err}')

def NukeDB():
    '''DELETE & Rebuild DabaBase'''
    if os.path.exists(DB_FILE):
        os.remove('DataBase/database.db')
        print("Nuked!")


if __name__ == '__main__':
    CreateDB()
    #NukeDB()

