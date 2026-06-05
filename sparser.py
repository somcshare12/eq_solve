from operator import truediv
from Eq_Evaluator import Eq_Evaluator

class Code_Parser:
    code_str = ""
    variables = {}

    def __init__(self, file_name):
        self.cal = Eq_Evaluator()
        self.file_name = file_name
        self.variables["pi"] = 3.14
        with open(self.file_name, "r", encoding="utf-8") as f:
            self.code_str = f.read()


    def parse(self):
        code_lines = self.code_str.split(";")
        trimmed_lines = [line.strip() for line in code_lines]
        print(trimmed_lines)
        for line in trimmed_lines:
            split_line2 = line.split("=")
            split_line = [sline.strip() for sline in split_line2]
            if(len(split_line) == 2):
                value = self.cal.evalute((split_line[1],self.variables))
                result = self.add_if_not_exists(split_line[0], value)
            #print(split_line)


    def add_if_not_exists(self,name, value):
        if not any(n == name for n in self.variables):
            self.variables[name] = value
            return True
        return False


    def print_variables(self):
        print(self.variables)

    def get_vaLue(self,var_name):
        return self.variables[var_name]