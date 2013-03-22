from eval import eval, Env
from parser import parse



def repl():
    while True:
        line = eval(parse(raw_input('$ ')))
        print line

if __name__ == '__main__':
    repl()

# (define a (lambda (x) (+ 1 1)))

# (define a (lambda (x) (lambda (y) (+ 1 1))))
