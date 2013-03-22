# (define (eval exp env)
#   (cond ((self-evaluating? exp) exp)
#         ((variable? exp) (lookup-variable-value exp env))
#         ((quoted? exp) (text-of-quotation exp))
#         ((assignment? exp) (eval-assignment exp env))
#         ((definition? exp) (eval-definition exp env))
#         ((if? exp) (eval-if exp env))
#         ((lambda? exp)
#          (make-procedure (lambda-parameters exp)
#                          (lambda-body exp)
#                          env))
#         ((begin? exp) 
#          (eval-sequence (begin-actions exp) env))
#         ((cond? exp) (eval (cond->if exp) env))
#         ((application? exp)
#          (apply (eval (operator exp) env)
#                 (list-of-values (operands exp) env)))
#         (else
#          (error "Unknown expression type -- EVAL" exp))))

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        return self if var in self else self.outer.find(var)

def add_globals(env):
    import math, operator as op
    env.update({
        '+': (lambda *args: reduce(op.add, args))})
    return env
global_env = add_globals(Env())

def eval(expr, env=global_env):
    if is_self_evaluating(expr):
        return expr
    elif isinstance(expr, str):
        return env.find(expr)[expr]
    elif is_assignment(expr):
        return eval_assignment(expr, env)
    elif is_definition(expr):
        return eval_definition(expr, env)
    elif is_lambda(expr):
        return eval_lambda(expr, env)
    elif is_quote(expr):
        return eval_quote(expr)
    elif is_application(expr):
        expr.pop(0)
        exps = [eval(exp, env) for exp in expr]
        procedure = exps.pop(0)
        return procedure(*exps)
    else:
        exps = [eval(exp, env) for exp in expr]
        procedure = exps.pop(0)
        return procedure(*exps)

def eval_assignment(expr, env):
    (_, var, val) = expr
    env.find(var)[var] = eval(val, env)

def eval_definition(expr, env):
    (_, var, val) = expr
    # FIXME: This is not quite right.
    env[var] = eval(val, env)

def eval_lambda(expr, env):
    (_, vars, exp) = expr
    return lambda *args: eval(exp, Env(vars, args, env))

def eval_quote(expr):
    (_, exps) = expr
    return exps

# Conditions
def is_self_evaluating(expr):
    if isinstance(expr, (float, int, long)) or is_string(expr):
        return True
    else:
        return False

def is_string(expression):
    if len(expression) > 2 and expression.count("\"") == 2:
        return True
    else:
        return False

def is_assignment(expression):
    return is_form(expression, "set")

def is_definition(expression):
    return is_form(expression, "define")

def is_application(expression):
    return is_form(expression, "apply")

def is_lambda(expression):
    return is_form(expression, "lambda")

def is_quote(expression):
    return is_form(expression, "quote")

def is_form(expression, form_name):
    if expression[0] == form_name:
        return True
    else:
        return False
