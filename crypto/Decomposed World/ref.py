from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


key = b'?'
iv = b'?'

#encrypt

FLAG = open('./FLAG.webp', 'rb').read()
cipher = AES.new(key = key, mode = AES.MODE_CBC, iv = iv)
ENC_FLAG = cipher.encrypt(pad(FLAG, 16))

with open('./ENC_FLAG', 'wb') as file:
    file.write(ENC_FLAG)

#decrypt

ENC_FLAG = open('./ENC_FLAG', 'rb').read()
decipher = AES.new(key = key, mode = AES.MODE_CBC, iv = iv)
DEC_FLAG = unpad(decipher.decrypt(ENC_FLAG),16)

with open('./DEC_FLAG.webp', 'wb') as file:
    file.write(DEC_FLAG)