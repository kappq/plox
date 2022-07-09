import sys
from tokens import TokenType, Token
from ast_printer import AstPrinter
from typing import Optional


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

        from parser import Parser

        parser = Parser(tokens)
        expression = parser.parse()

        if not expression:
            return

        print(AstPrinter().print(expression))

    @staticmethod
    def error(line: int, message: str, token: Optional[Token] = None) -> None:
        if token:
            if token.type == TokenType.EOF:
                Lox.report(token.line, " at end", message)
            else:
                Lox.report(token.line, f" at {token.lexeme!r}", message)
            return

        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        Lox.had_error = True


if __name__ == "__main__":
    Lox.main()
