from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import base64

def decipher(encrypted_media_url : str):
    cipher = DES.new(b'38346591', DES.MODE_ECB)
    decy = unpad(cipher.decrypt(base64.b64decode(encrypted_media_url)),block_size=8)
    return decy.decode()