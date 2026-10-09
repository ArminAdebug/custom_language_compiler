from logger import debug_log


class RegisterAllocation:
    all_registers = ("r10", "r11", "r12", "r13", "r14", "r15")

    def __init__(self):

        self.registers = list(RegisterAllocation.all_registers)

        self._reserve_to_add_registers = []

    def get_Register(self):
        for i in self._reserve_to_add_registers:
            if i in self.registers:
                raise RuntimeError("what the fuck")
        if not self.registers:
            raise RuntimeError("out of registers.")

        return self.registers.pop(0)

    def add_reserved_registers(self):

        for register in self._reserve_to_add_registers:
            self.registers.insert(0, register)
            debug_log("added back", register)
        self._reserve_to_add_registers.clear()

    def reserve_to_add_register(self, register):
        if register in RegisterAllocation.all_registers:
            self._reserve_to_add_registers.append(register)

        else:
            raise NameError(
                f"unknown register wants to add to reservation list <{register}>.")


class SolveExprition:
    def __init__(self, vars: dict[str, str], funcs: dict[str, str], ra: RegisterAllocation, code_section: list[str]):
        self.vars = vars
        self.funcs = funcs
        self.ra = ra
        self.code_section = code_section

    def solve(self, line) -> str:

        exprition_list = self.make_list_from_statement(line)
        if len(exprition_list) == 1:
            return exprition_list
        elif not exprition_list:
            raise RuntimeError("Excepted a exprition!")
        out = self.solve_tree(exprition_list)

        if out in self.ra.all_registers:
            self.ra.reserve_to_add_register(out)
            self.ra.add_reserved_registers()

        return out

    def solve_tree(self, exprition_list: list) -> list:

        debug_log(f"{exprition_list=}")
        while any([type(i) == list for i in exprition_list]):
            for i, item in enumerate(exprition_list):
                if type(item) == list:
                    out = self.solve_tree(item)
                    exprition_list[i] = out

        out = self.solve_statement(exprition_list)

        return out

    def solve_statement(self, exprition: list[list | str]):

        debug_log(f"solving statement: {exprition}\n")

        while len(exprition) > 1:

            for i, c in enumerate(exprition):
                if c in ("*", "/", "%"):
                    debug_log(exprition[i-1], exprition[i], exprition[i+1])
                    # 2 + 3 = i-1 : 2, i: +, i+1: 3
                    out = self.make_operation(
                        self.check_item(exprition[i-1]),
                        exprition[i],
                        self.check_item(exprition[i+1]))

                    exprition[i-1:i+2] = [out]

                    break
            else:
                for i, c in enumerate(exprition):
                    if c in ("+", "-"):
                        # 2 + 3 = i-1 : 2, i: +, i+1: 3
                        out = self.make_operation(
                            self.check_item(exprition[i-1]),
                            exprition[i],
                            self.check_item(exprition[i+1])
                        )

                        exprition[i-1:i+2] = [out]

                        break

        return exprition[0]

    def find_number(self, i: int, n: str):

        c = "0"
        o = ""
        while c.isnumeric() and i < len(n):
            c = n[i]

            if not c.isnumeric():
                break

            o += c
            i += 1
        return o

    def find_name(self, i: int, n: str):

        c = "a"
        o = ""
        while c.isalpha() and i < len(n):
            c = n[i]

            if not c.isalpha():
                break

            o += c
            i += 1
        return o

    def make_list_from_statement(self, n: str):

        # (2 + (3 + 5 )) + (1 + 5)
        out = []

        i = 0
        while i < len(n):
            c = n[i]

            if c == "(":
                d = 0
                b_i = i
                i += 1
                while d >= 0:
                    c = n[i]
                    if c == " ":
                        i += 1
                        continue

                    if c == "(":
                        d += 1
                    elif c == ")":
                        d -= 1

                    i += 1

                out.append(self.make_list_from_statement(n[b_i+1:i-1]))

            elif c.isdigit():

                number = self.find_number(i, n)
                out.append(number)

                i += len(number)

            elif c.isalpha():
                number = self.find_name(i, n)
                out.append(number)

                i += len(number)

            elif c != " ":
                out.append(c)

            i += 1

        return out

    def check_item(self, n):
        if n in RegisterAllocation.all_registers:
            debug_log("reserved to add:", n)
            self.ra.reserve_to_add_register(n)
        return n

    def make_operation(self, n1 : int, n2 : str, n3 : int):

        all_reserved_names = list(self.vars.keys()) + list(self.funcs.keys()) + list(self.ra.all_registers)
        if n1 not in all_reserved_names and n3 not in all_reserved_names:
            return eval(f"{n1} {n2} {n3}")


        n1 = f"[{n1}]" if n1 in self.vars else n1
        n3 = f"[{n3}]" if n3 in self.vars else n3

        register = self.ra.get_Register()
        self.code_section.append("")

        debug_log("using register:", register)

        if n2 == "+":
            self.code_section.append(f"mov {register}, {n1}")
            self.code_section.append(f"add {register}, {n3}")
        if n2 == "-":
            self.code_section.append(f"mov {register}, {n1}")
            self.code_section.append(f"sub {register}, {n3}")
        if n2 == "*":
            self.code_section.append(f"mov {register}, {n1}")
            self.code_section.append(f"imul {register}, {n3}")

        if n2 in ("/", "%"):

            self.code_section.append("push rbx")
            self.code_section.append("push rax")

            if n2 == "%":
                self.code_section.append("push rdx")

            self.code_section.append(f"mov rax, {n1}")
            self.code_section.append("cqo")
            self.code_section.append(f"mov rbx, {n3}")
            self.code_section.append(f"idiv rbx")

            self.code_section.append(
                f"mov {register}, {"rax" if n2 == "/" else "rdx"}")

            if n2 == "%":
                self.code_section.append("pop rdx")
            self.code_section.append("pop rax")
            self.code_section.append("pop rbx")

        self.ra.add_reserved_registers()

        return register


# test
if __name__ == "__main__":
    test5 = "(5 * baba) + (((50 + 4) * 2 - 3 / 9 / 5) - 6)"

    test = "(50 + 4) * 2 - 3 / 9"

    print(test)

    ra = RegisterAllocation()

    output = []
    SolveExprition.solve(test)

    print("\n".join(output))
