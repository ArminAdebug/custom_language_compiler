
class ErrorHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def syntax_error(self, line, col, massage=""):

        self._log_error("Syntax Error", massage or "corrupted syntax.", (line, col))

    def unknown_statement_error(self, line):
        self._log_error("syntax Error", "unknown statement.")
        
    def name_error(self, massage):

        self._log_error("name error", massage or "wrong name")

    def _log_error(self, error_type, error_massage, line_col : tuple[int] | None = None):

        print(f"compile failed!")
        print(f"Error in {self.file_path}")

        if all(line_col):
            print(f"line: {line_col[0]+1}, col: {line_col[1]+1}")
            with open(self.file_path, "r") as f:
                print(f.readlines()[line_col[0]])

        print("=" * 10)
        print(f"{error_type}: {error_massage}")

