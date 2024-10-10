from Crypto.Util.number import getPrime, isPrime, bytes_to_long

p = 0
q = 0
while(True):
    p = getPrime(512)
    q = p**2 + p + 1
    if isPrime(q):
        break

r = getPrime(1024)

n = p * q * r
e = 65537

m = bytes_to_long(open("./flag.txt", 'r').read().encode())
c = pow(m, e, n)

def reduce_mod_pm(n, a):
    r = n % a
    if r > (a >> 1):
        r -= a
    return r

def decompose(r, a, q):
    r  = r % q
    r0 = reduce_mod_pm(r, a)
    r1 = r - r0
    if r1 == q - 1:
        return 0, r0 - 1
    r1 = r1 // a
    assert r == r1*a + r0
    return r1, r0

a = 1<<128

print('n : ', n)
print('e : ', e)
print('(High Bit, Low Bits) : ',(decompose(c, a, n)))