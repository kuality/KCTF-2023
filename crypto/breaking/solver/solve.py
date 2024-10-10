from pwn import *
from randcrack import RandCrack
context.log_level = 'debug'
if sys.argv[1] == '1':
    io = remote('localhost', 6161)
else:
    io = remote('ctf.kuality.kr', 11111)
rc = RandCrack()

def get_rand():
    io.sendlineafter('> ', '1')
    io.recvline()
    return int(io.recvline().split(b' : ')[1])

def quiz(num):
    io.sendlineafter('> ', str(num))

rands = [get_rand() for _ in range(624)]
for i in range(624):
    rc.submit(rands[i])
print(rands)
io.sendlineafter('> ', '2')
for _ in range(100):
    t = rc.predict_getrandbits(32)
    quiz(t)

io.recvline()
FLAG = io.recvline().decode().strip()
print(FLAG)
assert FLAG == 'KCTF{5d830d1d4201b047b979cec1504bade0948896ad285194b1c6842bfeb22aaa78cdf3e21369487a1a1005cb05b941c443a3e9a32bebc7b675ad1023a3f092d9ba}'