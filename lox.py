import sys


class Lox:
    had_error = False

    @staticmethod
    def main() -> None:
        args = sys.argv[1:]
        if len(args) > 1:
            print("Usage: plox [script]")
        elif len(args) == 1:
            Lox.run_file(args[0])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(path: str) -> None:
        with open(path) as file:
            contents = file.read()
            Lox.run(contents)

            if Lox.had_error:
                exit(65)

    @staticmethod
    def run_prompt() -> None:
        while True:
            line = input("> ")
            if line is None:
                break
            Lox.run(line)
            Lox.had_error = False

    @staticmethod
    def run(source: str) -> None:
        from scanner import Scanner

        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str) -> None:
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        Lox.had_error = True


if __name__ == "__main__":
    Lox.main()
