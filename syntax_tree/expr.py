from dataclasses import dataclass


@dataclass
class Expr:
    def accept(self) -> str:
        pass


def parenthesize(name, expressions: list[Expr]) -> str:
    result = ""

    result += f"({name}"

    for expr in expressions:
        result += " "
        result += expr.accept()

    result += ")"

    return result
