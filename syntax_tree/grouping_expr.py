from dataclasses import dataclass
from syntax_tree.expr import Expr, parenthesize


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept(self) -> str:
        return parenthesize("group", [self.expression])
