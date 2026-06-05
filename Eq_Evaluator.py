import math

class Eq_Evaluator:
    # test ka saman
    functions = ['sin', 'cos', 'tan']
    global eqify
    eqify = False


    def tokenizer(self, eq):
        tokens = []
        i = 0
        self.eqify = False
        self.n_variable = None

        while i < len(eq):
            c = eq[i]

            if c.isspace():
                i += 1
                continue
            #negative?
            if c == "-" and (len(tokens) == 0 or tokens[-1] in ["+", "-", "*", "^", "/", "(", ")", "="]):
                if i+1 < len(eq) or (eq[i+1].isdigit() or eq[i+1] == "."):
                    start = i
                    i += 1
                    while i<len(eq) and (eq[i+1].isdigit() or eq[i+1] == "."):
                        i += 1
                    if i < len(eq) and eq[i] in "Ee":
                        i += 1
                        if i < len(eq) and eq[i] in "+-":
                            i += 1
                        while i < len(eq) and eq[i].isdigit():
                            i += 1
                    tokens.append(eq[start:i])
                    continue
            #normal numbers
            if c.isdigit() or c == ".": #incase u use stuff like .5 .10
                start = i
                while i < len(eq) and (eq[i].isdigit() or eq[i] == "."):
                    i += 1
                if i < len(eq) and eq[i] in "Ee":
                    i += 1
                    if i < len(eq) and eq[i] in "+-":
                        i += 1
                    while i < len(eq) and eq[i].isdigit():
                        i += 1
                tokens.append(eq[start:i])
                continue
            #variables, functions etc
            if c.isalpha():
                start = i
                while i < len(eq) and eq[i].isalpha():
                    i += 1
                tokens.append(eq[start:i])
                continue
            #operators
            if c in "+-*/^(),=":
                tokens.append(c)
                i += 1
                continue
            #raise ValueError("Unknown Character" + c)
        if "=" in tokens:
            tokens = self.equalsign(tokens)
            self.eqify = True
        else:
            self.eqify = False
        return tokens

    def equalsign(self, tokens):
        self.eqify = True
        self.n_variable = None
        index = tokens.index("=")
        global n_variable
        n_variable = tokens[:index]
        equation = tokens[index+1:]
        return equation

    def isdigitcursed(self, current, variables, functions):
        if current in variables:
            return True
        else:
            try:
                float(current)
                return True
            except:
                return False


    def isfunction(self, current):
        bracket_count = 0
        for b in current:
            if b == "(":
                bracket_count += 1
            elif b == ")":
                bracket_count += 1
            else:
                pass
        if bracket_count == 2:
            return True
        else:
            return False


    def substitution(self, thing, variables):
        bracket_count = 0
        for b in thing:
            if b in "()":
                bracket_count += 1
            elif b in variables and bracket_count > 0:  # bug what if there is an x in the func itself T-T
                thing = thing.replace(b, str(variables[b]))
        return thing


    def runfunction(self, bruh, variables):
        sub_ver = self.substitution(bruh, variables)
        if sub_ver.startswith('sin('):
            return math.sin(float(sub_ver[4:-1]))
        elif sub_ver.startswith('cos('):
            return math.cos(float(sub_ver[4:-1]))
        elif sub_ver.startswith('tan('):
            return math.tan(float(sub_ver[4:-1]))


    def convert_rpn(self, equation, output, variables, functions):
        operations_stack = []
        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3
        }

        for current in equation:
            if self.isdigitcursed(current, variables, functions):
                output.append(current)
            elif current in functions:
                operations_stack.append(current)
            elif current == "(":
                operations_stack.append(current)
            elif current == ")":
                while operations_stack and operations_stack[-1] != "(":
                    output.append(operations_stack.pop())
                operations_stack.pop()

                if operations_stack and operations_stack[-1] in self.functions:
                    output.append(operations_stack.pop())
            else:
                if len(operations_stack) > 0:
                    while operations_stack and operations_stack[-1] != "(" and operations_stack[-1] not in functions and (
                            precedence[operations_stack[-1]] > precedence[current] or (
                            precedence[operations_stack[-1]] == precedence[current] and current != "^")):
                        a = operations_stack.pop()
                        output.append(a)
                operations_stack.append(current)

        while len(operations_stack) > 0:
            output.append(operations_stack.pop())
        return output


    def evaluate_rpn(self, rpn, output, variables, functions):
        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3
        }
        for current in rpn:
            current = str(current)
            if current.isdigit() or self.isdigitcursed(current, variables, functions):
                if "." in current:
                    output.append(float(current))
                elif current in "Ee":
                    current = current.split("E")
                    bleh = 10 ** float(current[1])
                    current = float(current[0]) * bleh
                    output.append(current)
                elif current in variables:
                    current = variables[current]
                    output.append(current)
                else:
                    output.append(int(current))
            elif current in functions:
                value = output.pop()

                if current == "sin":
                    output.append(math.sin(value))
                elif current == "cos":
                    output.append(math.cos(value))
                elif current == "tan":
                    output.append(math.tan(value))
            else:
                second_no = float(output.pop())
                first_no = float(output.pop())
                if current == "+":
                    result = first_no + second_no
                if current == "-":
                    result = first_no - second_no
                if current == "*":
                    result = first_no * second_no
                if current == "/":
                    result = first_no / second_no
                if current == "^":
                    result = first_no ** second_no
                output.append(result)
                if eqify == True:
                    variables[n_variable] = result
        return output


    def evalute(self, test):
        functions = ['sin', 'cos', 'tan']
        variables = test[1]
        output = []
        outputil = []
        og_equation = self.tokenizer(test[0])
        rpn_equation = self.convert_rpn(og_equation, output, variables, functions)
        solved_answer = self.evaluate_rpn(rpn_equation, outputil, variables, functions)
        return solved_answer[0]

