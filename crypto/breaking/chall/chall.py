from secret import FLAG
import random
def menu():
    print('1. get random')
    print('2. quiz')
    print('3. exit')
    sel = int(input('> '))
    return sel

def main():
    WIN = 100
    i=0
    while True:
        sel = menu()
        match sel:
            case 1:
                print(f'rand : {random.getrandbits(32)}')
            case 2:
                win = 0
                while True:
                    if win == WIN:
                        print(FLAG.decode())
                        exit(0)
                    print(f'Stage {i}, win : {win}')
                    i+=1
                    number = int(input('> '))
                    if random.getrandbits(32) == number:
                        win += 1
            case 3:
                print('Bye!')
                exit(0)
            case _:
                exit(1)

if __name__ == '__main__':
    main()