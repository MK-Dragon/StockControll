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
        debug_flask_server.info(f'\t{user_info}')

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
    print('/DeliverItem -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'Decrypted: {entry_data}')

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
        else:
            resp = {
                'status': 'False'
            }
        # Encrypt and Send
        resp = DEncrypt.encrypt_to_json(resp)
        return jsonify(resp)
    except Exception as err:
        debug_flask_server.error(f'Error: {err}')

@app.route('/restock', methods=['POST'])
def ReStock_posted():
    print('/ReStock -> posted')
    try:
        # Get & decrypt data
        entry_data = request.get_json()
        entry_data = DEncrypt.decrypt_from_json(entry_data)
        debug_flask_server.info(f'Decrypted: {entry_data}')

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
        else:
            resp = {
                'status': 'False'
            }
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

@app.route('/delivereditem', methods=['GET'])
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
    return resp




# ?? Remove or Edit ??

@app.route('/items', methods=['GET'])
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
        debug_flask_server.error('\tNo JSON Item Received')



if __name__ == '__main__':
   app.run(debug=True) # add host='0.0.0.0' to use it on LAN