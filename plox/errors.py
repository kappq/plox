from tokens import Token


class ParseError(RuntimeError):
    pass


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message
