from expr import Expr, ExprVisitor, Binary, Grouping, Literal, Unary
from tokens import Token, TokenType
from typing import Any


class AstPrinter(ExprVisitor):
    @staticmethod
    def main() -> None:
        expression = Binary(
            Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Literal(123),
            ),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67)),
        )

        print(AstPrinter().print(expression))

    def print(self, expr: Expr) -> Any:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        builder = "(" + name
        for expr in exprs:
            builder += " "
            builder += expr.accept(self)
        builder += ")"

        return builder

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)


if __name__ == "__main__":
    AstPrinter.main()
