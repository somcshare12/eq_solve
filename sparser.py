import math

from Eq_Evaluator import Eq_Evaluator


class Code_Parser:
    def __init__(self, file_name):
        self.cal = Eq_Evaluator()
        self.file_name = file_name
        self.variables = {"pi": math.pi}
        with open(self.file_name, "r", encoding="utf-8") as f:
            self.code_str = f.read()

    def parse(self):
        for statement in self._statements():
            name, expression = self._split_assignment(statement)
            self.variables[name] = self.cal.evaluate((expression, self.variables))
        return self.variables

    def _statements(self):
        normalized_source = self.code_str.replace(";", "\n")
        return [
            statement.strip()
            for statement in normalized_source.splitlines()
            if statement.strip()
        ]

    def _split_assignment(self, statement):
        parts = [part.strip() for part in statement.split("=", 1)]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(f"Invalid assignment statement: {statement}")
        if not parts[0].isidentifier():
            raise ValueError(f"Invalid variable name: {parts[0]}")
        return parts[0], parts[1]

    def add_if_not_exists(self, name, value):
        if name not in self.variables:
            self.variables[name] = value
            return True
        return False


    def print_variables(self):
        print(self.variables)

    def get_value(self, var_name):
        return self.variables[var_name]

    def get_vaLue(self, var_name):
        return self.get_value(var_name)