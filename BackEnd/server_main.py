# Flask as API
from flask import Flask, jsonify, request
import json
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
# TODO: Encrypt and Decrypt JSON String

@app.route('/login', methods=['GET'])
def login():
    debug_flask_server.info('/login')
    try:
        user_info = request.get_json(force=True)
        debug_flask_server.info(f'\t{user_info}')

        if db.Validate_Login(user=user_info['user'], password=user_info['password']):
            resp = [{
                'login': True,
                'worker': db.Read_Full_Table('colaboradores'),
                'storage': db.Read_Full_Table('armarios'),
                'items': db.Read_Full_Table('items')
            }]
            return jsonify(resp)
        else:
            resp = [{
                'login': False,
                'error': "Wrong user or Password",
                'failed_loging': 1
            }]
            return jsonify(resp)
    except:
        debug_flask_server.error('\tNo JSON Item Received (?)')


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
   app.run(debug=True)