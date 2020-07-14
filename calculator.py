import math

class SmartCalculator:
    variables = {}
    command = ""

    def __init__(self):
        self.variables = dict()

    def parse(self, command):
        self.command = command
        self.clean()
        return self.evaluate(self.command)

    def clean(self):
        while "--" in self.command or "-+" in self.command or "++" in self.command or "+-" in self.command:
            self.command = self.command.replace("--", '+').replace("-+", "-").replace("+-", "-").replace('++', '+')
        self.command = self.command.replace('-', ' - ').replace('+', ' + ').replace('*', ' * ').replace('/', ' / ')\
            .replace('(', ' ( ').replace(')', ' ) ').replace('^', ' ^ ')
        while "  " in self.command:
            self.command = self.command.replace("  ", " ")

    def variable_assignment(self):
        key, value = self.command.split("=", 1)
        if key.strip().isalpha():
            if value.strip() not in self.variables.keys() and not value.strip().isdigit():
                return "Invalid identifier"
            elif value.strip().isalpha():
                self.variables[key.strip()] = self.evaluate(value.strip())
            elif value.strip().isnumeric():
                self.variables[key.strip()] = int(value.strip())
            else:
                return "Invalid assignment"

        else:
            return "Invalid identifier"
        return

    def evaluate(self, command):
        if "=" in command:
            return self.variable_assignment()
        elif command.isalpha():
            if command in self.variables.keys():
                return self.variables[command]
            else:
                return "Unknown variable"
        else:
            for var, value in self.variables.items():
                command = command.replace(var, str(value))
            postfix = self.postfix_evaluate(self.to_postfix(command))
            return postfix

    @staticmethod
    def to_postfix(infix):
        stack = []
        result = []
        operators = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1, ')': 1, '^': 4}
        for element in infix.split():
            if element not in operators.keys():
                result.append(element)
            else:
                if element == '(':
                    stack.append(element)
                elif element == ')':
                    operator = stack.pop()
                    while operator != '(':
                        result.append(operator)
                        operator = stack.pop()
                else:
                    while len(stack) != 0:
                        if operators[stack[-1]] >= operators[element]:
                            result.append(stack.pop())
                        else:
                            break
                    stack.append(element)
        while len(stack) != 0:
            result.append(stack.pop())
        return " ".join(result)

    def postfix_evaluate(self, postfix):
        stack = []
        operators = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1, ')': 1, '^': 4}
        for element in postfix.split():
            if element not in operators.keys():
                stack.append(int(element))
            else:
                stack.append(self.calculate(element, stack.pop(), stack.pop()))
        return stack.pop()

    @staticmethod
    def to_infix(postfix):
        stack = []
        operators = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1, ')': 1, '^': 4}
        for e in postfix.split():
            if e not in operators.keys():
                stack.append(e)
            else:
                oper1 = stack.pop(-2)
                oper2 = stack.pop()
                if e == "/":
                    # /pf 3 8 4 3 + 2 * 1 + * + 6 2 1 + / -
                    # /pf abc-+de-fg-h+/*
                    if any(oper in oper1 for oper in operators.keys()):
                        oper1 = f"({oper1})"
                    if any(oper in oper2 for oper in operators.keys()):
                        oper2 = f"({oper2})"
                    stack.append(f"{oper1}{e}{oper2}")
                elif e == "*":
                    if any(oper in oper1 for oper in operators.keys()):
                        oper1 = f"({oper1})"
                    if any(oper in oper2 for oper in operators.keys()):
                        oper2 = f"({oper2})"
                    stack.append(f"{oper1}{e}{oper2}")
                else:
                    stack.append(f"{oper1}{e}{oper2}")
        return stack.pop()

    @staticmethod
    def calculate(element, param, param1):
        if element == "*":
            return param1 * param
        elif element == "/":
            return int(param1 / param)
        elif element == "-":
            return param1 - param
        elif element == "+":
            return param1 + param
        elif element == "^":
            return int(math.pow(param1, param))


smartcalc = SmartCalculator()
while True:
    command = input()
    if command.startswith("/"):
        if command == "/exit":
            break
        if command.startswith("/pf"):
            print(smartcalc.to_infix(command.replace("/pf ", '').replace("", " ").replace("  ", " ")))
            continue
        elif command == "/help":
            print("The program calculates the sum of numbers, supports variables and subtraction")
            continue
        else:
            print("Unknown command")
            continue
    if command == "":
        continue
    if command.startswith(" ") and "=" not in command:
        print("Unknown variable")
        continue
    try:
        if " " in command and not ("+" in command or "=" in command or "-" in command or "*" in command or "/" in command or "^" in command):
            print(1)
            raise ValueError
        if command.endswith('+') or command.endswith('-'):
            print(2)
            raise ValueError
        if command.count("(") != command.count(")"):
            print(3)
            raise ValueError
        if "**" in command or "//" in command:
            print(4)
            raise ValueError
        result = smartcalc.parse(command)
        if result or result == 0:
            print(result)
    except ValueError:
        print("Invalid expression")
print("Bye!")
