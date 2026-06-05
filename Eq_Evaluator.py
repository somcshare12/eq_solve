import math


class Eq_Evaluator:
    functions = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
    }
    operators = {
        "+": (1, "left"),
        "-": (1, "left"),
        "*": (2, "left"),
        "/": (2, "left"),
        "^": (3, "right"),
    }
    unary_operators = {
        "neg": (2.5, "right"),
    }

    def tokenizer(self, eq):
        tokens = []
        i = 0

        while i < len(eq):
            c = eq[i]

            if c.isspace():
                i += 1
                continue

            if c.isdigit() or c == ".":
                number, i = self._read_number(eq, i)
                tokens.append(number)
                continue

            if c.isalpha() or c == "_":
                start = i
                i += 1
                while i < len(eq) and (eq[i].isalnum() or eq[i] == "_"):
                    i += 1
                tokens.append(eq[start:i])
                continue

            if c in "+-*/^(),=":
                tokens.append(c)
                i += 1
                continue

            raise ValueError(f"Unknown character: {c}")

        return tokens

    def _read_number(self, eq, start):
        i = start
        saw_digit = False

        while i < len(eq) and (eq[i].isdigit() or eq[i] == "."):
            saw_digit = saw_digit or eq[i].isdigit()
            i += 1

        if i < len(eq) and eq[i] in "Ee":
            exp_start = i
            i += 1
            if i < len(eq) and eq[i] in "+-":
                i += 1
            exp_digits_start = i
            while i < len(eq) and eq[i].isdigit():
                i += 1
            if exp_digits_start == i:
                raise ValueError(f"Invalid number: {eq[start:i]}")
            saw_digit = saw_digit or exp_start > start

        number = eq[start:i]
        if not saw_digit:
            raise ValueError(f"Invalid number: {number}")

        float(number)
        return number, i

    def equalsign(self, tokens):
        if tokens.count("=") != 1:
            raise ValueError("Expressions can contain only one assignment")

        index = tokens.index("=")
        variable = tokens[:index]
        equation = tokens[index + 1:]

        if len(variable) != 1 or not self._is_identifier(variable[0]):
            raise ValueError("Assignment target must be a single variable name")
        if not equation:
            raise ValueError("Assignment is missing a right-hand expression")

        return variable[0], equation

    def isdigitcursed(self, current, variables, functions=None):
        return self._is_number(current) or current in variables

    def isfunction(self, current):
        return current in self.functions

    def substitution(self, thing, variables):
        tokens = self.tokenizer(thing)
        substituted = [
            str(variables[token]) if token in variables else token
            for token in tokens
        ]
        return "".join(substituted)

    def runfunction(self, bruh, variables):
        return self.evaluate((bruh, variables))

    def convert_rpn(self, equation, output=None, variables=None, functions=None):
        output = [] if output is None else output
        variables = {} if variables is None else variables
        functions = self.functions if functions is None else {
            name: self.functions[name] for name in functions
        }
        operations_stack = []
        previous_token = None

        for current in equation:
            if self._is_number(current) or (
                self._is_identifier(current) and current not in functions
            ):
                if self._is_identifier(current) and current not in variables:
                    raise NameError(f"Unknown variable: {current}")
                output.append(current)
            elif current in functions:
                operations_stack.append(current)
            elif current == ",":
                while operations_stack and operations_stack[-1] != "(":
                    output.append(operations_stack.pop())
                if not operations_stack:
                    raise ValueError("Misplaced comma or mismatched parentheses")
            elif current == "(":
                operations_stack.append(current)
            elif current == ")":
                while operations_stack and operations_stack[-1] != "(":
                    output.append(operations_stack.pop())
                if not operations_stack:
                    raise ValueError("Mismatched parentheses")
                operations_stack.pop()

                if operations_stack and operations_stack[-1] in functions:
                    output.append(operations_stack.pop())
            elif current in self.operators:
                if current in "+-" and self._is_unary(previous_token):
                    if current == "-":
                        operations_stack.append("neg")
                    previous_token = current
                    continue

                while (
                    operations_stack
                    and self._is_operator(operations_stack[-1])
                    and self._should_pop_operator(operations_stack[-1], current)
                ):
                    output.append(operations_stack.pop())
                operations_stack.append(current)
            else:
                raise ValueError(f"Unknown token: {current}")

            previous_token = current

        while operations_stack:
            operator = operations_stack.pop()
            if operator == "(":
                raise ValueError("Mismatched parentheses")
            output.append(operator)

        return output

    def evaluate_rpn(self, rpn, output=None, variables=None, functions=None):
        output = [] if output is None else output
        variables = {} if variables is None else variables
        functions = self.functions if functions is None else {
            name: self.functions[name] for name in functions
        }

        for current in rpn:
            if self._is_number(current):
                output.append(float(current))
            elif current in variables:
                output.append(float(variables[current]))
            elif current in functions:
                if not output:
                    raise ValueError(f"Function {current} is missing an argument")
                output.append(functions[current](output.pop()))
            elif current in self.unary_operators:
                if not output:
                    raise ValueError(f"Operator {current} is missing an operand")
                output.append(-output.pop())
            elif current in self.operators:
                if len(output) < 2:
                    raise ValueError(f"Operator {current} is missing operands")
                second_no = output.pop()
                first_no = output.pop()
                output.append(self._apply_operator(current, first_no, second_no))
            else:
                raise NameError(f"Unknown variable: {current}")

        if len(output) != 1:
            raise ValueError("Expression did not reduce to a single value")

        return output

    def evaluate(self, test):
        equation, variables = test
        variable_name = None
        tokens = self.tokenizer(equation)

        if "=" in tokens:
            variable_name, tokens = self.equalsign(tokens)

        rpn_equation = self.convert_rpn(tokens, variables=variables)
        solved_answer = self.evaluate_rpn(rpn_equation, variables=variables)[0]

        if variable_name is not None:
            variables[variable_name] = solved_answer

        return solved_answer

    def evalute(self, test):
        return self.evaluate(test)

    def _apply_operator(self, operator, first_no, second_no):
        if operator == "+":
            return first_no + second_no
        if operator == "-":
            return first_no - second_no
        if operator == "*":
            return first_no * second_no
        if operator == "/":
            return first_no / second_no
        if operator == "^":
            return first_no ** second_no
        raise ValueError(f"Unknown operator: {operator}")

    def _is_number(self, value):
        try:
            float(value)
        except (TypeError, ValueError):
            return False
        return True

    def _is_identifier(self, value):
        return isinstance(value, str) and value.isidentifier()

    def _is_unary(self, previous_token):
        return (
            previous_token is None
            or previous_token in self.operators
            or previous_token in {"(", "=", ","}
        )

    def _should_pop_operator(self, stack_operator, current_operator):
        stack_precedence, _ = self._operator_info(stack_operator)
        current_precedence, associativity = self._operator_info(current_operator)
        return stack_precedence > current_precedence or (
            stack_precedence == current_precedence and associativity == "left"
        )

    def _is_operator(self, token):
        return token in self.operators or token in self.unary_operators

    def _operator_info(self, token):
        if token in self.operators:
            return self.operators[token]
        return self.unary_operators[token]
