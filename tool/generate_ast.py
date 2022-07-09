import sys
from io import TextIOWrapper


NEWLINE = "\n"
INDENTATION = "    "


class GenerateAst:
    @staticmethod
    def main() -> None:
        args = sys.argv[1:]
        if len(args) != 1:
            print("Usage: generate_ast <output directory>")
            exit(64)
        output_dir = args[0]
        GenerateAst.define_ast(
            output_dir,
            "Expr",
            {
                "Binary": "left: Expr, operator: Token, right: Expr",
                "Grouping": "expression: Expr",
                "Literal": "value: Any",
                "Unary": "operator: Token, right: Expr",
            },
        )

    @staticmethod
    def define_ast(output_dir: str, base_name: str, types: dict[str, str]) -> None:
        path = f"{output_dir}/{base_name.lower()}.py"

        with open(path, "w") as file:
            file.write("from abc import ABC, abstractmethod")
            file.write(NEWLINE)
            file.write("from typing import Any")
            file.write(NEWLINE)
            file.write("from tokens import Token")
            file.write(NEWLINE)
            file.write("from __future__ import annotations")
            file.write(NEWLINE * 3)
            file.write(f"class {base_name}(ABC):")
            file.write(NEWLINE)
            file.write(INDENTATION + "@abstractmethod")
            file.write(NEWLINE)
            file.write(
                INDENTATION + f"def accept(self, visitor: {base_name}Visitor) -> None:"
            )
            file.write(NEWLINE)
            file.write(INDENTATION * 2 + "pass")
            file.write(NEWLINE * 3)

            GenerateAst.define_visitor(file, base_name, types)

            for class_name, fields in types.items():
                file.write(NEWLINE * 2)
                GenerateAst.define_type(file, base_name, class_name, fields)

    @staticmethod
    def define_type(
        file: TextIOWrapper, base_name: str, class_name: str, fields: str
    ) -> None:
        file.write(f"class {class_name}({base_name}):")
        file.write(NEWLINE)
        file.write(INDENTATION + f"def __init__(self, {fields}) -> None:")
        file.write(NEWLINE)

        for field in fields.split(", "):
            name = field.split(": ")[0]
            file.write(INDENTATION * 2 + f"self.{name} = {name}")
            file.write(NEWLINE)

        file.write(NEWLINE)
        file.write(
            INDENTATION + f"def accept(self, visitor: {base_name}Visitor) -> None:"
        )
        file.write(NEWLINE)
        file.write(
            INDENTATION * 2
            + f"return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)"
        )
        file.write(NEWLINE)

    @staticmethod
    def define_visitor(
        file: TextIOWrapper, base_name: str, types: dict[str, str]
    ) -> None:
        file.write(f"class {base_name}Visitor(ABC):")

        name = base_name.lower()
        for type_name in types:
            file.write(NEWLINE)
            file.write(INDENTATION + "@abstractmethod")
            file.write(NEWLINE)
            file.write(
                INDENTATION
                + f"def visit_{type_name.lower()}_{name.lower()}(self, {name.lower()}: {type_name}) -> None:"
            )
            file.write(NEWLINE)
            file.write(INDENTATION * 2 + "pass")
            file.write(NEWLINE)


if __name__ == "__main__":
    GenerateAst.main()
