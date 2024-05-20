# Flask as API
from flask import Flask, jsonify, request
#import json
import DEncrypt
# DataBase Manager
import DataBase_Manager as db
# Extras
import logging


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

debug_flask_server = setup_logger('flask server', 'logs/flaskserver.log')
debug_flask_server.info('---//---')

app = Flask(__name__)



# Login and Authentication:
@app.route('/login', methods=['GET'])
def login():
    debug_flask_server.info('/login')
    try:
        user_info = request.get_json() # force=True
        user_info = DEncrypt.decrypt_from_json(user_info)

        # Log user_info...(?)
        debug_flask_server.info(f'\t{user_info["user"]}')

        login_info = db.Validate_Login(user=user_info['user'], password=user_info['password'])

        if login_info[0]:
            resp = {
                'login': True,
                'user_id': login_info[1],
                'worker': db.Read_Full_Table('colaboradores'),
                'storage': db.Read_Full_Table('armarios'),
                'items': db.Read_Full_Table('items')
            }
            resp = DEncrypt.encrypt_to_json(resp)
            return resp #jsonify(resp)
        else:
            resp = {
                'login': False,
                'error': "Wrong user or Password",
                'failed_loging': 1
            }
            resp = DEncrypt.encrypt_to_json(resp)
            return resp #jsonify(resp)
    except:
        debug_flask_server.error('\tNo JSON Item Received (?)')



# Add Entries:

@app.route('/deliveritem', methods=['POST'])
def DeliverItem_posted():
    debug_flask_server.info('/DeliverItem -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status = db.Deliver_Item(
            user_id=entry_data['user_id'],
            worker_id=entry_data['worker_id'],
            item_id=entry_data['item_id'],
            num= -entry_data['num'],
            storage_id=entry_data['storage_id']
        )

        # response:
        if status:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')

@app.route('/restock', methods=['POST'])
def ReStock_posted():
    debug_flask_server.info('/ReStock -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status = db.ReStock(
            user=entry_data['user_id'],
            storage_source_id=entry_data['storage_source'],
            storage_restocked_id=entry_data['storage_restock'],
            item_id=entry_data['item_id'],
            units=entry_data['num']
        )

        # response:
        if status:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')


# Add Item, Storage, Workers and Users

@app.route('/additem', methods=['POST'])
def add_item():
    # TODO: needs testing
    debug_flask_server.info('/Adding Item -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status_item = db.Add_Item(
            item_name=entry_data['item_name'],
            description=entry_data['item_desc']
        )

        # response:
        if status_item:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')

@app.route('/addstorage', methods=['POST'])
def add_storage():
    #TODO: needs testing
    debug_flask_server.info('/Adding Storage -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status_item = db.Add_Storage(
            name=entry_data[''],
            location=entry_data['']
        )

        # response:
        if status_item:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')

@app.route('/addworker', methods=['POST'])
def add_worker():
    #TODO: needs testing
    debug_flask_server.info('/Adding Worker -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status_item = db.Add_Worker(
            name=entry_data['worker_name'],
            number=entry_data['worker_num']
        )

        # response:
        if status_item:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')

@app.route('/adduser', methods=['POST'])
def add_user():
    #TODO: needs testing
    debug_flask_server.info('/Adding User -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status_item = db.Add_User(
            username=entry_data[''],
            password=entry_data['']
        )

        # response:
        if status_item:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')


# + First Stock
@app.route('/addfirststock', methods=['POST'])
def add_first_stock():
    #TODO: needs testing
    debug_flask_server.info('/Adding First Stock -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status_f_stock = db.Add_First_Stock_Entry(
            storage_id=entry_data['storage_id'],
            item_id=entry_data['item_id'],
            unit_min=entry_data['unit_min'],
            unit_max=entry_data['unit_max']
        )

        # response:
        if status_f_stock:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase: {status_f_stock = }')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')


# Get Information:

@app.route('/reload', methods=['GET'])
def reload_data():
    # TODO do Special read for users with only usernames! NO PASSWORDS!!!
    resp = {
        'worker': db.Read_Full_Table('colaboradores'),
        'storage': db.Read_Full_Table('armarios'),
        'items': db.Read_Full_Table('items'),
        'stock': db.Read_Full_Table('stock'),
        'restock': db.Complex_Read_Table(
            table='restock',
            num_results=50,
            order_by='id',
            order_desc=True
        ),
        'delivered': db.Complex_Read_Table(
            table='entrega',
            num_results=50,
            order_by='id',
            order_desc=True
        )
    }
    resp = DEncrypt.encrypt_to_json(resp)
    return resp



# ?? Remove or Edit ??

# not in use...
'''@app.route('/addfirstrestock', methods=['POST'])
def add_first_restock():
    #TODO: needs testing
    debug_flask_server.info('/Adding First Restock -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status_f_stock = db.Add_First_Stock_Entry(
            storage_id=entry_data[''],
            item_id=entry_data[''],
            unit_min=entry_data[''],
            unit_max=entry_data['']
        )
        status_restock = db.ReStock(
            user=entry_data[''],
            storage_source_id=entry_data[''],
            storage_restocked_id=entry_data[''],
            item_id=entry_data[''],
            units=entry_data['']
        )


        # response:
        if status_f_stock and status_restock:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase: {status_f_stock = } and {status_restock = }')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')

@app.route('/addfirstdeliveritem', methods=['POST'])
def add_first_deliver_item():
    debug_flask_server.info('/DeliverItem -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'\tDecrypted: {entry_data}')

        # Save data do DataBase
        status_f_stock = db.Add_First_Stock_Entry(
            storage_id=entry_data[''],
            item_id=entry_data[''],
            unit_min=entry_data[''],
            unit_max=entry_data['']
        )
        status = db.Deliver_Item(
            user_id=entry_data['user_id'],
            worker_id=entry_data['worker_id'],
            item_id=entry_data['item_id'],
            num= -entry_data['num'],
            storage_id=entry_data['storage_id']
        )

        # response:
        if status:
            resp = {
                'status': 'True'
            }
            debug_flask_server.info('\tSuccessfully Saved')
        else:
            resp = {
                'status': 'False'
            }
            debug_flask_server.error(f'\tFailed to save to DataBase')
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')'''


# Not in use...
"""@app.route('/delivereditem', methods=['GET'])
def get_delivered_items_data():
    resp = {
        'delivered': db.Complex_Read_Table(
            table='entrega',
            num_results=50,
            order_by='id',
            order_desc=False
        )
    }
    resp = DEncrypt.encrypt_to_json(resp)
    return resp

@app.route('/restock', methods=['GET'])
def get_restock_data():
    resp = {
        'restock': db.Complex_Read_Table(
            table='restock',
            num_results=50,
            order_by='id',
            order_desc=False
        )
    }
    resp = DEncrypt.encrypt_to_json(resp)
    return resp

@app.route('/restock', methods=['GET'])
def get_stock_data():
    resp = {
        'stock': db.Complex_Read_Table(
            table='stock',
            #num_results=50,
            order_by='id',
            order_desc=True
        )
    }
    resp = DEncrypt.encrypt_to_json(resp)
    return resp"""


# Deprecated???
"""@app.route('/items', methods=['GET'])
def get_employees():
    data = db.Read_Full_Table('items')
    debug_flask_server.info('/items response:')
    for d in data:
        debug_flask_server.info(f'\t{d}')
    return jsonify(data)



@app.route('/item/info', methods=['GET'])
def my_test_endpoint():
    debug_flask_server.info('/item/info:')
    try:
        input_json = request.get_json(force=True)
        debug_flask_server.info(f'\t{input_json}')
        return db.Get_Stock_Data(item_id=input_json['id'])
    except:
        debug_flask_server.error('\tNo JSON Item Received')"""



if __name__ == '__main__':
    a, b = db.CreateDB()
    if a == b:
        debug_flask_server.info(f'DataBase Created [{a}/{b}]')
        db.Add_User('Admin', '123')
    elif a == 0:
        debug_flask_server.info(f'DataBase Already Exists [{a}/{b}]')
    else:
        debug_flask_server.error(f'Tables Created: [{a}/{b}]')
    app.run(debug=True, host='0.0.0.0') # add host='0.0.0.0' to use it on LAN