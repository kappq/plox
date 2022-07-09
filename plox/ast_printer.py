from expr import T, Expr, ExprVisitor, Binary, Grouping, Literal, Unary
from typing import Generic


class AstPrinter(ExprVisitor, Generic[T]):
    def print(self, expr: Expr) -> T:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        builder = "(" + name
        for expr in exprs:
            builder += " "
            builder += expr.accept(self)
        builder += ")"

        return builder

    def visit_binary_expr(self, expr: Binary) -> T:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> T:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> T:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> T:
        return self.parenthesize(expr.operator.lexeme, expr.right)
