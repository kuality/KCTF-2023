# Heart Bleed
* ### Category : Crypto
* ### Score : 300/300
* ### Solver : 0
* ### Host : Port
  * ctf.kuality.kr : 12321  
     
   
## Description  

I'm alive! Want to hear the sound of my heartbeat?

## Solution

CBC-MAC(Message Authentication Codes)은 상대방이 본인과 동일한 키를 가졌는지, 메시지가 위변조 되지 않았는지 등, 대상의 무결성(Integrity)을 검증하기 위해 사용된다.   

비밀키 $key$와 메시지 $m$이 있을 때, 해당 메시지의 태그 $t$는 $ENC_{AES}$($m$, $key$, $CBC$)의 하위 16 byte로 구성된다. 이는 메시지 $m$을 비밀키 $key$를 사용하여 AES-128-CBC로 암호화 한 암호문의 하위 16 byte가 태그 $t$임을 의미한다.   

이러한 CBC-MAC은 CBC-MAC 생성에 사용되는 **메시지의 길이가 고정되지 않을 경우** 아래와 같은 위변조 취약점이 존재한다.   
만약 두 개의 인증 쌍 ($m_1$, $t_1$)과 ($m_2$, $t_2$)가 존재할 경우, 이를 기반으로 생성한 메시지 $m = pad(m_1)||m_2^1 \oplus t_1||m_2^2||...$의 태그는 $t_2$임이 성립한다.   
   
따라서 해당 문제의 경우 2개의 메시지 $m_1$, $m_2$를 미리 생성한 후, cmd에 1을 입력하여 해당 메시지들의 태그 $t_1$과 $t_2$를 얻는다. 
```python 3
m1 = 0x10101010101010101010101010101010
m2 = 0x11111111111111111111111111111111
```

태그 $t_1$과 $t_2$를 아래와 같이 얻었다 가정하자.   
```python 3
t1 = 0xa71b86ac04afd707ee5480758a69d9ad
t2 = 0xe91cc3cdfb5349a7846a29001819e1ac
```
   
그러면 아래와 같은 코드를 통해 $m = pad(m_1)||m_2^1 \oplus t_1||m_2^2||...$인 메시지 $m$을 생성할 수 있다.   
```python 3
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.Padding import pad

m1 = 0x10101010101010101010101010101010
m2 = 0x11111111111111111111111111111111

pad_m1 = pad(bytes.fromhex('10101010101010101010101010101010'),16)
pad_m2 = pad(bytes.fromhex('11111111111111111111111111111111'),16)
m1_tag = 0xa71b86ac04afd707ee5480758a69d9ad
ans = m1_tag^m2

print(hex(bytes_to_long(pad_m1))[2:] + hex(ans)[2:])
``` 
생성된 메시지는 다음과 같다.   
```
1010101010101010101010101010101010101010101010101010101010101010b60a97bd15bec616ff4591649b78c8bc
```

이제 cmd에 2를 입력하여 메시지 인증을 진행하자.
메시지로는 위에서 생성한 메시지 값을, 태그 값은 t2를 사용한다.   
   
인증을 성공하면 doki doki Heartbeat가 시작된다. 해당 과정은 OpenSSL 1.0.1 버전에서 발견된 매우 위험한 취약점인 HaertBleed 취약점을 참고하여 간단하게 제작되었다.
대충 아무런 메시지를 입력해준 뒤, payload 길이를 입력한 메시지의 길이보다 훨씬 긴 길이를 입력해주면 서버에 저장된 모든 memory의 모든 값을 출력해준다. memory의 가장 앞에 문자열에 플래그가 저장되어있으므로 아래와 같은 결과를 출력한다.   
```
Please convey a message filled with love :) >> hello
Input your payload length >> 1000000000000
flag : KCTF{C00l!_Don't_W0rry,_My_H34rt_is_Stil1_W0rking!}I was about to read this post, but then I saw Daesanghyuk. Now, I have to worship... Even though I know I'll be wide awake once I start worshiping, I must worship. It is the calling of one devoted to Daesanghyuk. Alright, I'll begin the worship

Sorry I dragged you to show this .. Naruto Sasuke Fight Level really Is it true? It's a fight between the world's strongest. Is that Naruto like that? The real Naruto is a legend..Naruto became a strongest legendary hero in the world since he became a king, and he became a king, and he was thrilled. And .. In the theater version, Sasuke suddenly appeared in front of Kakashi in front of Kakashi and smashed it up and crushed it. I'm so impressed and I recently learned about Boruto. I'm sorry. I'm looking at the 20th episode now, but the real Naruto generation is so thrilling and everyone is so big that I have to say it's an unknown memory. Shino seems to be talking a lot. It's a good teacher .. And why is he bored? Boruto is cute, but he looks like Naruto. It's true that his character resembles. And if you hit the internet, is this a real fact ?? The enemy is a new monster in Boruto? Look at Naruto Sasuke's coalition. It's really coming out .. If it is real, it's a must see. It doesn't destroy the real world .. Wow, it was really tearing that Naruto Sasuke is going to be like that. Ha .. I really want to see Sasuke .. When did it really become the newest strongest? I think in the past, I think when I'm in the middle, something sad, good, emotional, and various emotions are complicated.

//Heartbleed...I'm dead:(..Oh you pierce my heart... Wouldn't you like to feel my heartbeat?           hello
```   

~~젠장... 또 대상혁이다...~~

다음과 같은 플래그를 얻을 수 있다.
```
KCTF{C00l!_Don't_W0rry,_My_H34rt_is_Stil1_W0rking!}
```





