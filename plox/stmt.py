from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from typing import Optional
from expr import Expr
from tokens import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor) -> Any:
        pass


class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: Block) -> Any:
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression) -> Any:
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: If) -> Any:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: Print) -> Any:
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: Var) -> Any:
        pass


class Block(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_block_stmt(self)


class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_expression_stmt(self)


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_if_stmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_print_stmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: Optional[Expr]) -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_var_stmt(self)
