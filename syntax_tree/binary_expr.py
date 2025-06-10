from dataclasses import dataclass

from interpreter.token import Token
from syntax_tree.expr import Expr, parenthesize


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self) -> str:
        return parenthesize(self.operator.lexeme, [self.left, self.right])
