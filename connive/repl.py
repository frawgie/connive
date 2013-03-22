import argparse
from eval import eval, Env
from parser import parse

def main():
    flags = parse_arguments()
    if flags.source != None:
        evaluate_file(flags.source)
    else:
        repl()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, help="Source file to run")
    return parser.parse_args()

def evaluate_file(source):
    fd = open(source, 'r')
    program = fd.read()
    tokenized = parse(program)
    print eval(tokenized)

def repl():
    while True:
        line = eval(parse(raw_input('$ ')))
        print line

if __name__ == '__main__':
    main()

