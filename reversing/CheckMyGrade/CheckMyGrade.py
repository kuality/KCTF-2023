import base64

def convert_pw(userinput):
    key = "cweoiqjcmdslknvoirejkfvopspfgdx"
    val = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(key,userinput))
    result = base64.b64encode(str.encode(val))
    pw_operations(result)
    return check_pw(result)

def pw_operations(data):
    for i in range(5):
        data = base64.b64encode(data)
        data = base64.b64decode(data)
    return data

def check_pw(result):
    checks = [
    result[1:3] == b"AB",
    len(result) > 10,
    result[-1:] == b"Z",
    ]
    if any(checks):
        print("condition met!")

    if result[0:4] == b"KDQx":
        if result[8:10] == b"Gl":
            if result[35:37] == b"iU":
                if result[15:18] == b"YH1":
                    if result[39:42] == b"XBQ":
                        if result[21:26] == b"B1AEA":
                            if result[4:8] == b"KRJB":
                                if result[27:31] == b"/EwR":
                                    if result[42:44] == b"==":
                                        if result[31:35] == b"cLxQ":
                                            if result[18:21] == b"opP":
                                                if result[37:39] == b"gN":
                                                    if result[26:27] == b"k":
                                                        if result[10:15] == b"AjOzd":
                                                            return True 
    else:
        return False

def login():
    userid = input("Enter your ID: ")
    password = input("Enter your password: ")
    if userid.startswith("user"):
        print("User ID verified!")
    else:
        print("User ID not recognized!")
    print("Checking system integrity...")
    for i in range(5):
        print(f"System check {i+1}/5: OK")
    if userid == "helloKCTF" and convert_pw(password):
        return True
    else:
        return False

def main():
    if login():
        print("You got flag!")
        print("Data Struncture : A+")
    else:
        print("Login failed")

def init_system():
    print("Initializing systems...")
    for _ in range(3):
        print("system initialized.")

if __name__ == "__main__":
    main()
