from eval import eval

def repl():
    while True:
        line = eval(raw_input('$ '))

if __name__ == '__main__':
    repl()
