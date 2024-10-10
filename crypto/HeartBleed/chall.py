import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class Server:
    def __init__(self):
        f = open("./flag.txt","r")
        self.memory = ''
        
        self.memory += 'flag : ' + f.read()
        f.flush()
        f.close()

        f = open("./memory.txt","r")
        self.memory += f.read()
        f.flush() 
        f.close()

    def response(self, payload):
        self.memory += payload[0]
        return self.memory[-payload[1]:]
    
    def CBC_MAC_GEN(self, m, k, iv):
        input_m = pad(m,16)
        cipher = AES.new(key = k, mode = AES.MODE_CBC, iv = iv)
        t = cipher.encrypt(input_m)[-16:].hex()
        return (m,t)

    def Verify(self, m, t, k, iv, dup):
        verify_m = pad(m,16)
        cipher = AES.new(key = k, mode = AES.MODE_CBC, iv = iv)
        t1 = cipher.encrypt(verify_m)[-16:].hex()

        if(t == t1):
            if m in dup:
                print('Well... this is known message... please try another message')
                return False
            else:
                return True
        else :
            print('Invalid Identifier')
            return False


def main():
    key = os.urandom(16)
    s = Server()

    iv = bytes.fromhex('00'*16)
    Known_message = []
    while(True):
        command = input('cmd >> ')
        try:
            if(command == '0'):
                print('Bye~ :)')
                break

            elif(command == '1'):
                message = bytes.fromhex(input('m(hex) >> '))
                Known_message.append(message)
                print('(message, tag) : ', s.CBC_MAC_GEN(message,key,iv))
                
            elif(command == '2'):
                message = bytes.fromhex(input('m(hex) >> '))
                tag = input('t(hex) >> ')
                if(s.Verify(message, tag, key, iv, Known_message)):
                    print('running doki doki Heartbeat')
                    message = input('Please convey a message filled with love :) >> ')
                    len_payload = int(input('Input your payload length >> '))
                    payload = (message, len_payload)
                    print(s.response(payload))
                else:
                    continue            
            else:
                print('Please input a number among 0, 1, 2 :) ')

        except:
            print('?')

if __name__ == '__main__':
    main()



    

