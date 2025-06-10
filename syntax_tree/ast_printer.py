from syntax_tree.expr import Expr


class AstPrinter:
    def print(self, expr: Expr) -> str:
        return expr.accept()
