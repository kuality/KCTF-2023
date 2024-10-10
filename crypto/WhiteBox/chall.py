from sage.all import GF, Matrix, det, vector, random_matrix
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import numpy as np
import os

Sbox = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
            )

MC0_T = np.array([2,1,1,3])
MC1_T = np.array([3,2,1,1])
MC2_T = np.array([1,3,2,1])
MC3_T = np.array([1,1,3,2])

MUL2 = lambda a : (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def MUL(a, b):
    r = 0
    tmp = b
    for i in range(8):
        if(a & 1):
            r ^= tmp
        tmp = MUL2(tmp)
        a = (a >> 1)
    return r

# 1 x 4 vector
def Mat_MUL(MC, v):
    res = np.zeros(4, dtype=int)
    for i in range(4):
        res[i] = MUL(MC[i],v)
    return res

def gen_linear_mapping():
    while(True):
        map = random_matrix(GF(2), 32, 32)
        if(det(map) != 0):
            return map
        
def encoding(s, linear_map):
    s_ = vector(GF(2), 32)
    for i in range(4):
        for j in range(8):
            s_[8*i+j] = (s[i]>>j)&1
    s_ = s_ * linear_map

    res = 0
    for i in range(32):
        res = (res<<1)|int(s_[i])
    return res

TMC0_T = np.zeros(256, dtype=int)
TMC1_T = np.zeros(256, dtype=int)
TMC2_T = np.zeros(256, dtype=int)
TMC3_T = np.zeros(256, dtype=int)

encode = [gen_linear_mapping() for i in range(4)]

for i in range(256):
    TMC0_T[i] = encoding(Mat_MUL(MC0_T, Sbox[i]), encode[0])
    TMC1_T[i] = encoding(Mat_MUL(MC1_T, Sbox[i]), encode[1])
    TMC2_T[i] = encoding(Mat_MUL(MC2_T, Sbox[i]), encode[2])
    TMC3_T[i] = encoding(Mat_MUL(MC3_T, Sbox[i]), encode[3])

def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]

class Server:
    def __init__(self):
        self.seed = [bytes_to_long(os.urandom(1)) for i in range(16)]
        f = open('./flag.txt', 'r')
        self.flag = f.read()
        f.flush()
        f.close()

    def decompose_seed(self):
        key = b''
        for i in range(16):
            key += long_to_bytes(self.seed[i])
        return key
    
    def chall(self, key):
        flag = self.flag.encode()
        flag = pad(flag, 16)
        iv = bytes.fromhex('00'*16)
        cipher = AES.new(key = key, mode = AES.MODE_CBC, iv = iv)
        return cipher.encrypt(flag).hex()
    
    def error_injection(self, error):
        cipher = np.copy(np.reshape(error, (4, 4)))
        sec = np.copy(np.reshape(self.seed, (4, 4)))

        shift_rows(sec)
        shift_rows(cipher)

        add_round_key(cipher, sec)

        for i in range(4):
            cipher[i][0] = TMC0_T[cipher[i][0]]
            cipher[i][1] = TMC1_T[cipher[i][1]]
            cipher[i][2] = TMC2_T[cipher[i][2]]
            cipher[i][3] = TMC3_T[cipher[i][3]]

        cipher = np.reshape(cipher, 16)
        return cipher

def main():
    s = Server()
    cipher_flag = s.chall(s.decompose_seed())
    while(True):
        command = input('cmd >> ')
        try:
            if (command == '0'):
                print('Bye~ :)')
                break

            elif (command == '1'):
                error = [int(input()) for x in range(16)]
                if (len(error) != 16):
                    raise ValueError()
                print(error)
                print(s.error_injection(error))

            elif (command == '2'):
                print(cipher_flag)
            
            else:
                print('Please input a number among 0, 1, 2 :)')

        except:
            print('?')
        
if __name__ == '__main__':
    main()
    exit()



