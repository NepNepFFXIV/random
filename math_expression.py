import re
operators = {'+': 1, '-': 1, '*': 2, '/': 2, '~': 3}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def infix_to_postfix(string):
    postfix = []
    stack = []
    current_operand = ""
    unary_neg = False

    for character in string:
        if character.isdigit():
            current_operand += character
            continue
        
        if current_operand != "":
            postfix.append(current_operand)
            current_operand = ""

        if character == "(":
            stack.append("(")
        elif character == ")":
            while stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        else:
            if (not stack # stack is empty
                    or stack[-1] == "(" 
                    or operators[character] > operators[stack[-1]]):
                stack.append(character)
            else:
                while (stack 
                        and stack[-1] != "(" 
                        and operators[stack[-1]] >= operators[character]):
                    postfix.append(stack.pop())
                stack.append(character)

    if current_operand != "": postfix.append(current_operand)
    if unary_neg : postfix.append("~")

    while stack:
        postfix.append(stack.pop())
    
    return postfix

def evaluation(a, b, op):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/": return a / b
    if op == "~": return a - b
    raise Exception(f"Operator {op} not supported")

def postfix_evaluation(postfix):
    stack = []
    for item in postfix:
        if is_number(item):
            stack.append(float(item))
        elif item == "~":
            n1 = stack.pop()
            stack.append(evaluation(0, float(n1), item))
        else:
            n2 = stack.pop()
            n1 = stack.pop()
            stack.append(evaluation(float(n1), float(n2), item))
    return stack[-1]

def calc(expression):
    transform = lambda c: "~"+c.group(2) if len(c.group(1)) & 1 == 1 else c.group(2)
    expression = re.sub(r'\s', '', expression)
    expression = re.sub(r'^(-)|((?<=\()-)|((?<=[+\-*/])-)', r'~', expression)
    expression = re.sub(r'(~+)([^~]*)', transform, expression)
    
    postfix = infix_to_postfix(expression)

    return postfix_evaluation(postfix)

print(calc("(10)"))
print(calc('10- 2- -5'))
print(calc("-7 * -(6 / 3)"))
