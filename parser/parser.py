from dataclasses import dataclass
from interpreter.token import Token
from syntax_tree.expr import Expr


@dataclass
class Parser:
    tokens: list[Token]
    current: int = 0

    def expression(self) -> Expr:
        # TODO
        return Expr()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]
