import re
'''Test'''

class Stack:
    def __init__(self, size):
        self.stack = []
        self.size = size

    def push(self, item):
        if len(self.stack) < self.size:
            self.stack.append(item)

    def pop(self):
        result = -1
        if self.stack != []:
            result = self.stack.pop()
        return result

    def return_list(self):
        return self.stack

    def isEmpty(self):
        return self.stack == []

    def topChar(self):
        result = -1

        if self.stack != []:
            result = self.stack[len(self.stack) - 1]

        return result


variables = dict()


def plus(a, b):
    return a + b


def minus(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    try:
        return int(a / b)
    except:
        return a / b


def pow(a, b):
    return a ** b


def sign(a):
    if a == '-' * len(a):
        if a.count('-') % 2 == 0:
            return '+'
        else:
            return '-'
    else:
        return '+'


def to_digit(c):
    try:
        return int(c)
    except:
        try:
            return float(c)
        except:
            return False


def check_var(a):
    try:
        return variables[a]
    except KeyError:
        return False


def check_id(a):
    if a.isalpha():
        return True
    else:
        return False


def isfloat(value):
    if '.' in value:
        try:
            float(value)
            return True
        except ValueError:
            return False
    else:
        return False


def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def isOperand(c):
    if c.isalpha() or c.isdigit() or isfloat(c):
        return True
    try:
        float(c)
        int(c)
        return True
    except:
        return False


operators = "+-*/^"


def isOperator(operation):
    return operation in operators


def getPrecedence(c):
    result = 0

    for char in operators:
        result += 1

        if char == c:
            if c in '-/':
                result -= 1
            break
    return result


def toPostfix(expression):
    result = Stack(100)

    stack = Stack(15)

    for char in expression:
        if char.count('*') > 1 or char.count('/') > 1:
            return False
        if char == '-' * len(char):
            char = sign(char)
        if char == '+' * len(char):
            char = '+'
        if isOperand(char):
            result.push(char)
        elif isOperator(char):
            while True:
                topChar = stack.topChar()

                if stack.isEmpty() or topChar == '(':
                    stack.push(char)
                    break
                else:
                    pC = getPrecedence(char)
                    pTC = getPrecedence(topChar)
                    if char != '^':
                        if pC > pTC:
                            stack.push(char)
                            break
                        else:
                            result.push(stack.pop())
                    else:
                        if pC >= pTC:
                            stack.push(char)
                            break
                        else:
                            result.push(stack.pop())

        elif char == '(':
            stack.push(char)
        elif char == ')':
            cpop = stack.pop()

            while cpop != '(':
                result.push(cpop)
                cpop = stack.pop()

        else:
            return False

    while not stack.isEmpty():
        cpop = stack.pop()
        result.push(cpop)
    return result


def calculation(expr):
    infix_str = expr.replace(" ", "")

    expr_list = re.split('([-+*/]+|[*/^()])', infix_str)
    result = list(filter(lambda a: a != '', expr_list))
    if result[0] == '-':
        result[1] = result[0] + result[1]
        result.pop(0)
    # print(result)
    if result.count('(') == result.count(')'):
        postfix = toPostfix(result)
    else:
        return "Invalid expression"

    calc = Stack(15)
    if postfix:
        for elem in postfix.return_list():
            if isfloat(elem):
                calc.push(float(elem))
            elif isint(elem):
                calc.push(int(elem))
            elif isOperator(elem):
                b = calc.pop()
                a = calc.pop()
                if elem == '-':
                    calc.push(minus(a, b))
                elif elem == '+':
                    calc.push(plus(a, b))
                elif elem == '*':
                    calc.push(mul(a, b))
                elif elem == '/':
                    calc.push(div(a, b))
                elif elem == '^':
                    calc.push(pow(a, b))
            else:
                if elem.isalpha():
                    if check_var(elem):
                        calc.push((check_var(elem)))
                    else:
                        return 'Unknown variable'
        else:
            return calc.pop()
    else:
        return "Invalid expression"


while True:
    command = input()
    if command == '':
        pass

    elif command[0] == '/':
        if command == '/exit':
            print('Bye!')
            break
        elif command == '/help':
            print('The program calculates the sum of numbers')
        else:
            print('Unknown command')

    elif command.isalpha():
        if check_var(command):
            print(variables[command])
        else:
            print('Unknown variable')

    # assignment
    elif '=' in command:
        if command.count('=') == 1:
            elem = [s.strip() for s in command.split('=')]
            key, value = elem[0], elem[1]
            if check_id(key):
                if isfloat(value):
                    variables[key] = float(value)
                elif value.isdigit():
                    variables[key] = int(value)
                elif value.isalpha():
                    if check_var(value):
                        variables[key] = variables[value]
                    else:
                        print('Unknown variable')
                else:
                    print('invalid assigment')
            else:
                print('invalid identifier')
        else:
            print('invalid assigment')
    else:
        print(calculation(command))
