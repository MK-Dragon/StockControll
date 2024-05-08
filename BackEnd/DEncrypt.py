import Encrypt_Decrypt
import json



def encrypt_to_json(data:dict, key = b'test_key_1245678') -> dict:
    '''
    takes a dict {}

    outputs:
    data_package = {
    'r4': '', (iv)
    'data': json encrypted data
}
    '''
    # data -> JSON String -> encrypt -> Return/send

    #data -> JSON String
    j_data = json.dumps(data, indent=4)

    #JSON String -> encrypt
    iv, encrypted_data = Encrypt_Decrypt.encriptar_dados(frase=j_data, chave=key)

    #encrypt -> Return / send
    Data_Package = {
        'r4': iv,
        'data': encrypted_data
    }
    return Data_Package

def decrypt_from_json(data_encrypted, key = b'test_key_1245678') -> dict:
    '''
    expects:
    data_package = {
    'r4': '', (iv)
    'data': json encrypted data
}
    '''
    # get data -> decrypt to json-> Json to dict -> Return/use

    #get data -> decrypt to json
    data_decrypted = Encrypt_Decrypt.desencriptar_dados(
        iv=data_encrypted['r4'],
        texto_encriptado=data_encrypted['data'],
        chave=key
    )

    #Json to dict -> Return/use
    clean_data = json.loads(data_decrypted)
    return clean_data




if __name__ == '__main__':
    data = {
        'name': 'Marco2',
        'pw': '12345'
    }

    print("\n\nSending and Receiving Encrypted data:\n")
    print(f'Original: {data}')
    data_to_send = encrypt_to_json(data)

    print(f'Encrypted data: {data_to_send}')

    data_received = decrypt_from_json(data_to_send)

    print(f'Data Decrypted: {data_received}')