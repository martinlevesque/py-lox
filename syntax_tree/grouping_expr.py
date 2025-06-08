from dataclasses import dataclass
from syntax_tree.expr import Expr


@dataclass
class GroupingExpr(Expr):
    def toto(self):
        print("toto")
        return ""
