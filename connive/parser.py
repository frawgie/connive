import ast


def parse(expr):
    """ Takes a string of s-expressions and converts it into a python list of
    symbols which can be used for evaluation. """
    return transform(tokenize(expr))


def tokenize(expr):
    return expr.replace('(', ' ( ').replace(')', ' ) ').split()


def transform(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF")

    first_token = tokens.pop(0)
    if first_token == '(':
        node = []
        while tokens[0] != ')':
            node.append(transform(tokens))
        tokens.pop(0)
        return node
    elif first_token == ')':
        raise SyntaxError("Unexpected )")
    else:
        return atom(first_token)
    return []


def atom(token):
    try: return int(token)
    except ValueError: pass
    try: return float(token)
    except: pass
    return token
