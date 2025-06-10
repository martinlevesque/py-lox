from dataclasses import dataclass

from interpreter.token import Token
from syntax_tree.expr import Expr, parenthesize


@dataclass
class UnaryExpr(Expr):
    operator: Token
    expression: Expr

    def accept(self) -> str:
        return parenthesize(self.operator.lexeme, [self.expression])
