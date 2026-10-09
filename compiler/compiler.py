from ast_parser import SolveExprition, RegisterAllocation
from errors import ErrorHandler

code_path = r"code.c$"
out = r"out.asm"


header = ["default rel"]
exit_zero_code = ["xor eax, eax", "ret"]

# var defines
data_section = []
bss_section = []
variables: dict[str, str] = {}
functions: dict[str, str] = {}

text_section = ["global main"]

# app code
main_section = []


def normal(n: str) -> str:
    n = n.strip()

    return n

# input etc: "int a = 5;"


def define_var(statement: str):

    if statement.startswith("int"):
        statement = normal(statement.split("int", 1)[1])

        if "=" in statement:
            name, value = statement.split("=", 1)

            name = normal(name)
            value = normal(value)

            if name[0].isdigit():
                error_handler.name_error("name connot start with digit.")

            data_section.append(f"{name} dq {value}")
            variables[name] = "int"

        else:
            bss_section.append(f"{statement} resb 4")
            variables[statement] = "int"


# input etc: "a = b * (c + 5);"


def assignment(statement: str):
    solve_exprition = SolveExprition(variables, functions, ra, main_section)
    name, value = statement.split("=", 1)

    name = normal(name)
    value = solve_exprition.solve(normal(value))

    if variables[name] == "int":
        if value in variables.keys():

            main_section.append(f"mov rcx, [{value}]")
            main_section.append(f"mov [{name}], rcx")

        else:
            main_section.append(f"mov [{name}], {value}")


# input etc: "add(1, 5);"
def function_call(statement: str):

    name, value = statement.split("=", 1)


def combine_asm_code() -> str:
    def add_tab(section): return ["\t" + l for l in section]

    code = []
    code += header

    if data_section:
        code.append("section .data")
        code += add_tab(data_section)

    if bss_section:
        code.append("section .bss_section")
        code += add_tab(bss_section)

    code.append("section .text")
    code += add_tab(text_section)

    code.append("main:")
    code += add_tab(main_section + exit_zero_code)

    return code


def seprate_statements(file: str) -> list[str]:
    statements = []

    depth = 0
    line = 0
    col = 0

    last_statement_index = 0
    is_string = False

    for i, c in enumerate(file, -1):
        # updating indexs
        if c == '\n':
            line += 1
            col = 0
        else:
            col += 1

        if c == "\"":
            is_string = not is_string
        if not c or is_string:
            continue

        # error handling
        if depth < 0:
            error_handler.syntax_error(line, col, "Extra Parenthesis.")

        # find statements
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1

        if not depth and c == ";":

            statements.append(
                normal(file[last_statement_index:i+1].replace("\n", "")))
            last_statement_index = i + 2

    return statements


def main():
    var_types = ("int", "str")

    # compile code line by line
    with open(code_path, "r") as f:
        code: list[str] = seprate_statements(f.read())

    for statement in code:

        if statement.split(" ", 1)[0] in var_types:
            define_var(statement)
            continue

        if statement.split(" ", 1)[0] in variables:
            assignment(statement)
            continue

        error_handler.unknown_statement_error()

    compiled_code: str = combine_asm_code()
    print("\n" * 3)
    print("\n".join(compiled_code))

    with open(out, "w") as f:
        f.write("\n".join(compiled_code))


if __name__ == "__main__":
    ra = RegisterAllocation()
    error_handler = ErrorHandler(file_path=code_path)
    main()
