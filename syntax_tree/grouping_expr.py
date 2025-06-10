from dataclasses import dataclass
from syntax_tree.expr import Expr


@dataclass
class GroupingExpr(Expr):
    expression: Expr
