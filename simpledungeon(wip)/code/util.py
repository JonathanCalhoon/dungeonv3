from code import terminal


def get_input(prompt, valid):
    while True:
        i = input(prompt).lower()

        if i in valid:
            return i
        else:
            print("Not a valid input!\n")


def get_int(_max=99999):
    while True:
        i = input()
        try:
            if int(i) <= _max:
                return int(i)
        except:
            pass


def floor(val):
    """Converts any Negative number to 0"""
    if val < 0:
        return 0
    else:
        return val



def center(string, max_length):
    if len(string) >= max_length:
        return string
    else:
        needed_chars = max_length-len(string)
        if needed_chars % 2 == 0:
            size = " "*int(needed_chars/2)
            return size+string+size
        else:
            size = " "*int(needed_chars/2)
            return size+" "+string+size


def indent(string, size):
    t = " "*int(size)
    print(t+string)

def cont():
    input("\n\nPress Enter to Continue")
    terminal.clear()

def cnt():
    input()
    terminal.clear()


def log(string):
    with open('log.txt', 'a+') as file:
        file.write("\n"+string)


def clear_log():
    with open('log.txt', 'w') as file:
        file.write("")