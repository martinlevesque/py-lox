from dataclasses import dataclass

from interpreter.token import Token, TokenType
from syntax_tree.expr import Expr


@dataclass
class LiteralExpr(Expr):
    literal: Token

    def accept(self) -> str:
        if self.literal.type == TokenType.TOKEN_TYPE_NIL:
            return "nil"
        else:
            return str(self.literal.lexeme)


def literal(
    type: TokenType = TokenType.TOKEN_TYPE_INVALID, value: str = "", line: int = 1
) -> LiteralExpr:
    literal_token = Token(type=type, lexeme=str(value), literal=str(value), line=line)
    return LiteralExpr(literal=literal_token)
