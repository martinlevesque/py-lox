from dataclasses import dataclass
from interpreter.token import Token, TokenType
from syntax_tree.grouping_expr import GroupingExpr
from syntax_tree.literal_expr import literal
from syntax_tree.expr import Expr
import sys


class ParseError(Exception):
    """Custom exception for parsing errors."""

    def __init__(self):
        super().__init__()


@dataclass
class Parser:
    tokens: list[Token]
    current: int = 0
    current_line: int = 1

    def expression(self) -> Expr:
        # TODO
        return Expr()

    # consumes the token if it is one of the types specified
    def match(self, types: list[TokenType]) -> bool:
        for t in types:
            if self.check(t):
                self.current_line = self.line()
                self.advance()
                return True

        return False

    def line(self) -> int:
        return self.tokens[self.current].line

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def isAtEnd(self) -> bool:
        return self.peek().type == TokenType.TOKEN_TYPE_EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1

        return self.previous()

    @staticmethod
    def error(token: Token, message: str) -> ParseError:
        if token.type == TokenType.TOKEN_TYPE_EOF:
            print(f"[{token.line}] at end, {message}", file=sys.stderr, flush=True)
        else:
            print(
                f"[{token.line}] at '{token.lexeme}' {message}",
                file=sys.stderr,
                flush=True,
            )

        return ParseError()

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()

        raise Parser.error(self.peek(), message)

    # true if the current token is of a given type
    def check(self, type: TokenType) -> bool:
        if self.isAtEnd():
            return False

        return self.peek().type == type

    # def term(self) -> Expr:

    # def factor(self) -> Expr:

    def primary(self) -> Expr | None:
        if self.match([TokenType.TOKEN_TYPE_FALSE]):
            return literal(
                type=TokenType.TOKEN_TYPE_FALSE,
                value=str(False),
                line=self.current_line,
            )

        if self.match([TokenType.TOKEN_TYPE_TRUE]):
            return literal(
                type=TokenType.TOKEN_TYPE_TRUE, value=str(True), line=self.current_line
            )

        if self.match([TokenType.TOKEN_TYPE_NIL]):
            return literal(
                type=TokenType.TOKEN_TYPE_NIL, value=str(None), line=self.current_line
            )

        if self.match([TokenType.TOKEN_TYPE_NUMBER, TokenType.TOKEN_TYPE_STRING]):
            return literal(
                type=self.previous().type,
                value=str(self.previous().literal),
                line=self.current_line,
            )

        if self.match([TokenType.TOKEN_TYPE_LEFT_PAREN]):
            expr: Expr = self.expression()
            self.consume(
                TokenType.TOKEN_TYPE_RIGHT_PAREN, "Expect ') after expression."
            )
            return GroupingExpr(expression=expr)

        return None
