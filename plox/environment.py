from __future__ import annotations
from typing import Any, Optional

from tokens import Token
from errors import LoxRuntimeError


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None) -> None:
        self.values: dict[str, Any] = {}
        self.enclosing = enclosing

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"undefined variable {name.lexeme}")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"undefined variable {name.lexeme}")

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value
