from xmlrpc.client import boolean
from dataclasses import dataclass
from interpreter.token import Token, TokenType
from syntax_tree.expr import Expr


@dataclass
class Parser:
    tokens: list[Token]
    current: int = 0

    def expression(self) -> Expr:
        # TODO
        return Expr()

    # consumes the token if it is one of the types specified
    def match(self, types: list[TokenType]) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def isAtEnd(self) -> bool:
        return self.peek().type == TokenType.TOKEN_TYPE_EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1

        return self.previous()

    # true if the current token is of a given type
    def check(self, type: TokenType) -> bool:
        if self.isAtEnd():
            return False

        return self.peek().type == type
