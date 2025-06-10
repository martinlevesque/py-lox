from dataclasses import dataclass

from interpreter.token import Token
from syntax_tree.expr import Expr


@dataclass
class UnaryExpr(Expr):
    operator: Token
    expr: Expr
