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
