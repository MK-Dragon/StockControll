# pip install pycryptodome
from Crypto.Cipher import AES  # Importação do módulo AES da biblioteca pycryptodome
from Crypto.Util.Padding import pad, unpad  # Importação de funções de preenchimento da biblioteca pycryptodome
import base64  # Importação da biblioteca base64 para codificação e decodificação

# TODO: Clean this up ^_^
def encriptar_dados(frase: str, chave = b'chave_16_bytes12') -> tuple:
    """
    Função para encriptar uma frase usando AES (Advanced Encryption Standard) em modo CBC (Cipher Block Chaining).

    Parâmetros:
    frase (str): A frase a ser encriptada.
    chave (bytes): A chave de encriptação.

    Retorna:
    tuple: Uma tupla contendo o vetor de inicialização (IV) e a frase encriptada.
    :return: (iv + texto_encriptado)
    """
    cifra = AES.new(chave, AES.MODE_CBC)  # Criação do objeto de cifra AES com a chave fornecida
    texto_encriptado = cifra.encrypt(pad(frase.encode(), AES.block_size))  # Encripta a frase e aplica o preenchimento
    iv = base64.b64encode(cifra.iv).decode('utf-8')  # Converte o IV para base64 e decodifica para string UTF-8
    texto_encriptado = base64.b64encode(texto_encriptado).decode('utf-8')  # Converte a frase encriptada para base64 e decodifica para string UTF-8
    return iv, texto_encriptado  # Retorna o IV e a frase encriptada como uma tupla

def desencriptar_dados(iv: str, texto_encriptado: str, chave = b'chave_16_bytes12') -> str:
    """
    Função para desencriptar uma frase usando AES (Advanced Encryption Standard) em modo CBC (Cipher Block Chaining).

    Parâmetros:
    iv (str): O vetor de inicialização (IV).
    texto_encriptado (str): A frase encriptada.
    chave (bytes): A chave de desencriptação.

    Retorna:
    str: A frase desencriptada.
    """
    iv = base64.b64decode(iv)  # Decodifica o IV de base64 para bytes
    texto_encriptado = base64.b64decode(texto_encriptado)  # Decodifica a frase encriptada de base64 para bytes
    cifra = AES.new(chave, AES.MODE_CBC, iv)  # Criação do objeto de cifra AES com a chave e o IV fornecidos
    frase_desencriptada = unpad(cifra.decrypt(texto_encriptado), AES.block_size)  # Desencripta a frase e remove o preenchimento
    return frase_desencriptada.decode('utf-8')  # Retorna a frase desencriptada como uma string UTF-8



if __name__ == "__main__":

    iv, data = encriptar_dados('Marco Polo')
    print(f'Frase: "Marco Polo"')
    print(f'\n\tiv: {iv}')
    print(f'\tdata: {data}\n')

    dados_decriptados = desencriptar_dados('Z5R2gKpZP62v2kFBVnDFlQ==', 'YrkLUeJrlBRYey5BU5JGYQ==')
    print(f'Dados: {dados_decriptados}')
