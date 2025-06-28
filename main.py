import sys

import scanner

from interpreter import token
from syntax_tree.expr import Expr
from parser.parser import Parser

# https://craftinginterpreters.com/parsing-expressions.html


class Interpreter:
    def __init__(self):
        self.has_error: bool = False

    def run(self, content: str):
        raw_tokens: list = scanner.scan_tokens(content)

        for t in raw_tokens:
            if t["err"]:
                print(f"err -> {t}")
            else:
                print(f"{t}")
                tt = token.load_token(t)
                print(f"tt -> {tt}")

        tokens = [token.load_token(t) for t in raw_tokens]

        parser: Parser = Parser(tokens)
        expression: Expr | None = parser.parse()

        if expression:
            print(expression)

    def run_file(self, filename: str):
        with open(filename, "r") as file:
            content = file.read()
            self.run(content)

            if self.has_error:
                sys.exit(65)

    def run_prompt(self):
        while True:
            self.out("> ")
            line = sys.stdin.readline()
            self.run(line)
            self.has_error = False

    def out(self, content: str):
        print(content, end="", flush=True)

    def error(self, line: int, message: str):
        self.report(line=line, where="", message=message)

    def report(self, line: int = 0, where: str = "", message: str = ""):
        print(
            f"[line {line}] Error {where}: {message}\n",
            file=sys.stderr,
            end="",
            flush=True,
        )


if __name__ == "__main__":
    interpreter = Interpreter()

    if len(sys.argv) > 2:
        interpreter.out("Usage: plox [script]\n")
        sys.exit(64)
    elif len(sys.argv) == 2:
        interpreter.run_file(sys.argv[1])
    else:
        interpreter.run_prompt()
