# WhiteBox
* ### Category : Crypto
* ### Score : 300/300
* ### Solver : 0
* ### Host : Port
  * ctf.kuality.kr : 12322  
     
   
## Description  

You don't have to know everything... Just one thing is important

## Solution   

$TMC$ 테이블의 구조는 아래와 같다.   


$TMC_0 = L_0 \circ MC_0 \circ Sbox_{AES}$   
$TMC_1 = L_1 \circ MC_1 \circ Sbox_{AES}$  
$TMC_2 = L_2 \circ MC_2 \circ Sbox_{AES}$   
$TMC_3 = L_3 \circ MC_3 \circ Sbox_{AES}$ 

   
$L_i \;(i \in \{0, 1, 2, 3\})$는 $GF(2)$의 원소로 이루어진 32-bit 입력 32-bit 출력의 Linear mapping이며 $i$마다 랜덤으로 생성된다.   
$MC_i$는 'MixColumns' 연산을 수행하는 행렬   

$MC = \begin{bmatrix}02 & 03& 01& 01 \\01 & 02& 03& 01 \\01 & 01& 02& 03 \\03 & 01& 01& 02 \\\end{bmatrix}$ 의 i번째 열을 의미한다.   

해당 $TMC_i$ 테이블에 입력되는 값은 'ShiftRow'연산과 'AddRoundKey' 연산이 적용된 값으로, 입력된 16 byte 평문을 $p$ , 16 byte 비밀키를 $k$라고 나타낼 때
$\widehat{p} \oplus \widehat{k}$ 이다. 여기서 hat 기호는 'ShiftRow'연산이 적용되었음을 의미한다.   
   
16byte의 평문 state는 아래와 같이 표현되며   

$state = \begin{bmatrix}p_0 & p_4& p_8& p_{12} \\p_1 & p_5& p_9& p_{13} \\p_2 & p_6& p_{10}& p_{14} \\p_3 & p_7& p_{11}& p_{15} \\\end{bmatrix}$   
   
   각 $state$의 원소 $p_j$는 $TMC_{s \\ mod \\ 4}(\widehat{p_j} \oplus \widehat{k_j})$로 mapping 된다.   
   $(j \in \{0, 1, ..., 15\},\ s = SR[j],\ SR = [ 0, 13, 10,  7,  4,  1, 14, 11,  8,  5,  2, 15, 12,  9,  6, 3])$   

본 문제는, 공격자가 입력한 $state$와 이를 통해 출력된 $TMC_{s \\ mod \\ 4}(\widehat{p_j} \oplus \widehat{k_j})$값을 통해 비밀키 $k$를 추출하는 것을 목표로 한다.   

비밀 인코딩 $L_i$ 때문에 $L_i$ 이전의 값이 무엇인지는 알 수 없지만, 만약 $TMC_{s\,mod\,4}(\widehat{p_j} \oplus \widehat{k_j}) = 0$일 경우 $MC_0 \circ Sbox_{AES}(\widehat{p_j} \oplus \widehat{k_j}) = 0$이며 $Sbox_{AES}(\widehat{p_j} \oplus \widehat{k_j}) =$ 역시 $0$이므로 \$\widehat{p_j} \oplus \widehat{k_j}$의 값이 0x52라는 것을 알 수 있다.   

$k_j$를 추출하기 위해 1 byte 크기의 전수 조사를 진행한다.   
$p_j = 0x52 \oplus a \in {0, 1, ... , 255}$로 선택한 뒤 $j$ 인덱스 이외의 다른 인덱스의 값은 $0$으로 하여 $state$를 초기화 한다. 만약 전수 조사 중 $TMC_{s \\ mod \\ 4}(\widehat{p_j} \oplus \widehat{k_j}) = 0$ 일 경우 $a = k_j$다. 이와 같은 방식으로 16번의 1 byte 전수 조사를 진행하면 해당 알고리즘은 $2^8 \cdot 2^4$의 work factor을 가지며 문제 상에서 seed 라고 불리는 $k$값을 온전히 추출해낼 수 있다.   
   
아래는 pwntools를 사용한 정답 코드다.   

``` python 
import pwn
import numpy as np
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from tqdm import tqdm

#r = pwn.process(['python3', './problem3.py'])
r = pwn.remote('ctf.kuality.kr', 12322)

def update(a):
    r.recvuntil('cmd >> ')
    r.sendline('1')

    for i in range(16):
        r.sendline(str(a[i]))

    r.recvline()
    val = r.recvuntil(']')
    cleaned_data = ''.join(chr(byte) for byte in val if chr(byte).isdigit() or chr(byte) in '- \n')

    number_strings = cleaned_data.split()

    val  = [int(num) for num in number_strings]
    return val

def update2():
    r.recvuntil('cmd >> ')
    r.sendline('2')
    enc = r.recvline()
    return enc

SR_index = [ 0, 13, 10,  7,  4,  1, 14, 11,  8,  5,  2, 15, 12,  9,  6, 3]
seed = []
error = list(range(16))
for i in tqdm(range(16)):
    hat = np.zeros(16, dtype=int)
    s_i = SR_index[i]
    for x in tqdm(range(256)):
        hat[i] = x^0x52
        if(update(hat)[s_i] == 0):
            seed.append(x)

def decompose_seed(seed):
        key = b''
        for i in range(16):
            key += long_to_bytes(seed[i])
        return key

cipher = AES.new(key = decompose_seed(seed), mode = AES.MODE_CBC, iv = bytes.fromhex('00'*16))
enc_flag = update2()
print(cipher.decrypt(bytes.fromhex(enc_flag.decode()[:-1])))
```
위의 코드를 실행시켜서 얻은 플래그는 아래와 같다.   
```
KCTF{L3aked_p4rtia1_1nf0rmation_0,_Th0ugh_Encoding...}
```
  
  
