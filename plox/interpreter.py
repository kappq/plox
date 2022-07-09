from expr import Expr, ExprVisitor, Literal, Grouping, Unary, Binary
from tokens import TokenType, Token
from lox import Lox
from typing import Any


class InterpretError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message


class Interpreter(ExprVisitor):
    def interpret(self, expression: Expr) -> None:
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except InterpretError as error:
            Lox.runtime_error(error.token.line, error.message)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self.is_truthy(right)

        return None

    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise InterpretError(
                    expr.operator, "operands must be two numbers or two strings"
                )
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

    def is_truthy(self, value: Any) -> bool:
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        return bool(a == b)

    def check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return

        raise InterpretError(operator, "operand must be a number")

    def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return

        raise InterpretError(operator, "operands must be a number")

    def stringify(self, value: Any) -> str:
        if value is None:
            return "nil"

        if isinstance(value, bool):
            return str(value).lower()

        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[0 : len(text) - 2]
            return text

        return str(value)
