# https://www.codewars.com/kata/52ffcfa4aff455b3c2000750

import re

precedence = {'=': 0, '+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
right_associativity = ['=']
brackets = '()'
keywords = ['fn', '=>']

def tokenize(expression):
    if expression == "":
        return []
    regex = re.compile(r"\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

def is_number(s):
    try:
        float(s)
    except ValueError:
        return False    
    return True

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def is_operand(self, s):
        return  s not in precedence \
                and s not in brackets \
                and s not in keywords \
                and s not in self.functions

    def check_operand(self, operand):
        if is_number(operand):
            return float(operand)
        if operand in self.functions and len(self.functions[operand]['args']) == 0:
            return self.functions[operand]['postfix'][0]
        if operand not in self.vars:
            raise KeyError(f"ERROR: Invalid identifier. No variable with name '{operand}' was found.")
        return self.vars[operand]

    def evaluate_bin_op(self, a, b, operator):
        b = self.check_operand(b)
        if operator == "=":
            if a in self.functions:
                raise ValueError(f"There is already a function with the name '{a}'")
            self.vars[a] = b
            return self.vars[a]

        a = self.check_operand(a)
        if operator == "+": return a + b
        if operator == "-": return a - b
        if operator == "*": return a * b
        if operator == "/": return a / b
        if operator == "%": return a % b
        
        raise Exception(f"Operator {operator} not supported")

    def eval_function(self, func_name, args):
        args_names = self.functions[func_name]['args']
        postfix = self.functions[func_name]['postfix']

        value_map = {k: v for k,v in zip(args_names, args)}        
        postfix = [i if i not in args_names else value_map[i] for i in postfix]
        return self.eval_postfix(postfix)

    def eval_postfix(self, tokens):
        stack = []
        for token in tokens:
            if self.is_operand(token):              # token is an operand
                stack.append(token)
            elif token in self.functions:           # token is a function
                num_args = len(self.functions[token]['args'])
                args = stack[-num_args:]
                stack = stack[:-num_args]
                stack.append(str(self.eval_function(token, args)))
            else:                                   # token is a binary operator
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(str(self.evaluate_bin_op(op1, op2, token)))
        return stack[-1]

    def infix_to_postfix(self, tokens):
        postfix, stack, func = [], [], []
        for token in tokens:
            if self.is_operand(token):
                postfix.append(token)
                while func:
                    func[-1][1] -= 1
                    if func[-1][1] == 0:                        
                        postfix.append(func.pop()[0])
                        continue
                    break                        
            elif token == '(':
                stack.append('(')
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            elif token in self.functions:
                num_args = len(self.functions[token]['args'])
                func.append([token, num_args])
            else:
                while   stack   \
                        and stack[-1] != '('    \
                        and precedence[stack[-1]] >= precedence[token] \
                        and token not in right_associativity:
                    postfix.append(stack.pop())
                stack.append(token)    
        return postfix + [i[0] for i in func[::-1]] + stack[::-1]    

    def is_valid_expression(self, postfix):
        counter = 0
        for token in postfix:
            if token in precedence:             # Binary operators
                counter -= 2
            elif token in self.functions:       # Functions
                num_args = len(self.functions[token]['args'])
                counter -= num_args
            if counter < 0:             
                return False
            counter += 1        
        return counter == 1

    def function_declaration(self, tokens):
        func_name = tokens[1]
        if func_name in self.vars:
            raise ValueError(f"There is already a variable with the name '{func_name}'")

        args, index = [], 2
        while tokens[index] != '=>':
            if tokens[index] in args:
                raise ValueError(f"There is already a parameter with the name '{tokens[index]}'") 
            args.append(tokens[index])
            index += 1
        expression = tokens[index+1:]
        
        postfix = self.infix_to_postfix(expression)
        for token in postfix:
            if self.is_operand(token) and not is_number(token) and token not in args:
                raise ValueError("Invalid expression input")

        if not self.is_valid_expression(postfix):
            raise ValueError("Invalid expression input")

        self.functions[func_name] = { "args": args, "postfix": postfix}
        return ''

    def input(self, expression):
        tokens = tokenize(expression)
        if not tokens:
            return ""

        if tokens[0] == 'fn':
            return self.function_declaration(tokens)

        postfix = self.infix_to_postfix(tokens)
        if len(postfix) == 1:
            return float(self.check_operand(postfix[0]))

        if self.is_valid_expression(postfix):
            return float(self.eval_postfix(postfix))
        raise ValueError("Invalid expression input")
        
if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.input("fn f1 a1 a2 => a1 * a2")
    interpreter.input("fn f2 a1 a2 a3 => a1 * a2 * a3")
    print(interpreter.input("f2 f2 1 2 3 f1 4 5 f1 6 7"))
    interpreter.input("fn avg a b c => (a + b + c) / 3")
    interpreter.input("fn add a b => a + b")
    interpreter.input("fn sub a b => a - b")
    print(interpreter.input("3 + avg 3 add 6 2 sub 3 2"))
