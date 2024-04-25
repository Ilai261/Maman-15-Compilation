from symbol_table import SymbolTable
from utils import DIVIDE, FLOAT, INT, MINUS, MULTIPLY, PLUS, is_float, is_integer

INT_VAR = "ti"
FLOAT_VAR = "tf"


class CodeGenerator:
    def __init__(self, symbol_table):
        self.variable_generator: VariableGenerator = VariableGenerator()
        self.lable_generator: LableGenerator = LableGenerator()
        self.symbol_table: SymbolTable = symbol_table

    def generate_assignment_stmt(self, expression_code, id, expression_var):
        generated_code = f"{expression_code}\n"
        if self.symbol_table.get_variable_type(id) == INT:
            generated_code += f"IASN {id} {expression_var}"
        elif self.symbol_table.get_variable_type(p.ID) == FLOAT:
            generated_code += f"RASN {id} {expression_var}"
        return generated_code

    def generate_expression(
        self, expression_code, expression_retval_var, addop, term_code, term_retval_var
    ):
        generated_code = f"{expression_code}\n{term_code}\n"
        if addop == PLUS:
            COMMAND = {INT: "IADD", FLOAT: "RADD"}
        else:
            COMMAND = {INT: "ISUB", FLOAT: "RSUB"}

        # both are integers
        if (
            expression_retval_var.startswith(INT_VAR)
            or is_integer(expression_retval_var)
        ) and (term_retval_var.startswith(INT_VAR) or is_integer(term_retval_var)):
            new_retval_var = (
                self.variable_generator.get_new_int_variable()
            )  # make sure variable is new
            generated_code += f"{COMMAND[INT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
            return generated_code, new_retval_var

        # both are floats
        elif (
            expression_retval_var.startswith(FLOAT_VAR)
            or is_float(expression_retval_var)
        ) and (term_retval_var.startswith(FLOAT_VAR) or is_float(term_retval_var)):
            new_retval_var = (
                self.variable_generator.get_new_float_variable()
            )  # make sure variable is new
            generated_code += f"{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
            return generated_code, new_retval_var

        # expression is float term is int, need to cast
        elif (
            expression_retval_var.startswith(FLOAT_VAR)
            or is_float(expression_retval_var)
        ) and (term_retval_var.startswith(INT_VAR) or is_integer(term_retval_var)):
            new_retval_var = (
                self.variable_generator.get_new_float_variable()
            )  # make sure variable is new
            if is_integer(term_retval_var):
                term_retval_var += ".0"
                generated_code += f"{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
                return generated_code, new_retval_var
            else:
                new_term = self.variable_generator.get_new_float_variable()
                generated_code += f"ITOR {new_term} {term_retval_var}\n{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {new_term}"
                return generated_code, new_retval_var

        # expression is int term is float, need to cast
        elif (
            expression_retval_var.startswith(INT_VAR)
            or is_integer(expression_retval_var)
        ) and (term_retval_var.startswith(FLOAT_VAR) or is_float(term_retval_var)):
            new_retval_var = (
                self.variable_generator.get_new_float_variable()
            )  # make sure variable is new
            if is_integer(expression_retval_var):
                expression_retval_var += ".0"
                generated_code += f"{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
                return generated_code, new_retval_var
            else:
                new_expression = self.variable_generator.get_new_float_variable()
                generated_code += f"ITOR {new_expression} {expression_retval_var}\n{COMMAND[FLOAT]} {new_retval_var} {new_expression} {term_retval_var}"
                return generated_code, new_retval_var

    def generate_term(
        self, term_code, term_retval_var, mulop, factor_code, factor_retval_var
    ):
        generated_code = f"{term_code}\n{factor_code}\n"
        if mulop == MULTIPLY:
            COMMAND = {INT: "IMLT", FLOAT: "RMLT"}
        else:
            COMMAND = {INT: "IDIV", FLOAT: "RDIV"}

        # both are integers
        if (term_retval_var.startswith(INT_VAR) or is_integer(term_retval_var)) and (
            factor_retval_var.startswith(INT_VAR) or is_integer(factor_retval_var)
        ):
            new_retval_var = (
                self.variable_generator.get_new_int_variable()
            )  # make sure variable is new
            generated_code += f"{COMMAND[INT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
            return generated_code, new_retval_var

        # both are floats
        elif (
            expression_retval_var.startswith(FLOAT_VAR)
            or is_float(expression_retval_var)
        ) and (term_retval_var.startswith(FLOAT_VAR) or is_float(term_retval_var)):
            new_retval_var = (
                self.variable_generator.get_new_float_variable()
            )  # make sure variable is new
            generated_code += f"{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
            return generated_code, new_retval_var

        # expression is float term is int, need to cast
        elif (
            expression_retval_var.startswith(FLOAT_VAR)
            or is_float(expression_retval_var)
        ) and (term_retval_var.startswith(INT_VAR) or is_integer(term_retval_var)):
            new_retval_var = (
                self.variable_generator.get_new_float_variable()
            )  # make sure variable is new
            if is_integer(term_retval_var):
                term_retval_var += ".0"
                generated_code += f"{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
                return generated_code, new_retval_var
            else:
                new_term = self.variable_generator.get_new_float_variable()
                generated_code += f"ITOR {new_term} {term_retval_var}\n{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {new_term}"
                return generated_code, new_retval_var

        # expression is int term is float, need to cast
        elif (
            expression_retval_var.startswith(INT_VAR)
            or is_integer(expression_retval_var)
        ) and (term_retval_var.startswith(FLOAT_VAR) or is_float(term_retval_var)):
            new_retval_var = (
                self.variable_generator.get_new_float_variable()
            )  # make sure variable is new
            if is_integer(expression_retval_var):
                expression_retval_var += ".0"
                generated_code += f"{COMMAND[FLOAT]} {new_retval_var} {expression_retval_var} {term_retval_var}"
                return generated_code, new_retval_var
            else:
                new_expression = self.variable_generator.get_new_float_variable()
                generated_code += f"ITOR {new_expression} {expression_retval_var}\n{COMMAND[FLOAT]} {new_retval_var} {new_expression} {term_retval_var}"
                return generated_code, new_retval_var


class VariableGenerator:
    # designates between int and float variable names
    def __init__(self):
        self.int_variable_count = 0
        self.float_variable_count = 0

    """ we need to add checks in symbol table here if variable already exists """

    def get_new_int_variable(self):
        var = f"{INT_VAR}{self.int_variable_count}"
        self.int_variable_count += 1
        return var

    def get_new_float_variable(self):
        var = f"{FLOAT_VAR}{self.float_variable_count}"
        self.float_variable_count += 1
        return var


class LableGenerator:
    def __init__(self):
        self.lable_count = 0

    def get_new_lable(self):
        lable = f"L{self.lable_count}"
        self.lable_count += 1
        return lable
