from Crypto.Util.number import *
from secret import FLAG # FLAG is ehre!

p = getPrime(1024)
q = getPrime(1024)

n = p * q
e = 0x10001

enc_list = []
enc_list = [pow(x, e, n) for x in FLAG]

print(f'n = {n}')
print(f'e = {e}')
print(f'enc = {enc_list}')