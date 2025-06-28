from dataclasses import dataclass
from interpreter.token import Token, TokenType
from syntax_tree.unary_expr import UnaryExpr
from syntax_tree.binary_expr import BinaryExpr
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

    def expression(self) -> Expr | None:
        return self.equality()

    def term(self) -> Expr | None:
        expr: Expr | None = self.factor()

        if not expr:
            return None

        while self.match([TokenType.TOKEN_TYPE_MINUS, TokenType.TOKEN_TYPE_PLUS]):
            operator: Token = self.previous()
            right: Expr | None = self.factor()

            if right:
                expr = BinaryExpr(left=expr, operator=operator, right=right)

        return expr

    def equality(self) -> Expr | None:
        expr: Expr | None = self.comparison()

        if not expr:
            return None

        while self.match(
            [TokenType.TOKEN_TYPE_BANG_EQUAL, TokenType.TOKEN_TYPE_EQUAL_EQUAL]
        ):
            operator: Token = self.previous()
            right: Expr | None = self.comparison()

            if right:
                expr = BinaryExpr(left=expr, operator=operator, right=right)

        return expr

    def factor(self) -> Expr | None:
        expr: Expr | None = self.unary()

        if not expr:
            return None

        while self.match([TokenType.TOKEN_TYPE_SLASH, TokenType.TOKEN_TYPE_STAR]):
            operator: Token = self.previous()
            right: Expr | None = self.unary()

            if right:
                expr = BinaryExpr(left=expr, operator=operator, right=right)

        return expr

    def unary(self) -> Expr | None:
        if self.match([TokenType.TOKEN_TYPE_BANG, TokenType.TOKEN_TYPE_MINUS]):
            operator: Token = self.previous()
            right: Expr | None = self.unary()

            if right:
                return UnaryExpr(operator=operator, expression=right)

        return self.primary()

    # consumes the token if it is one of the types specified
    def match(self, types: list[TokenType]) -> bool:
        for t in types:
            if self.check(t):
                self.current_line = self.line()
                self.advance()
                return True

        return False

    def comparison(self) -> Expr | None:
        expr: Expr | None = self.term()

        if not expr:
            return None

        token_types = [
            TokenType.TOKEN_TYPE_GREATER,
            TokenType.TOKEN_TYPE_GREATER_EQUAL,
            TokenType.TOKEN_TYPE_LESS,
            TokenType.TOKEN_TYPE_LESS_EQUAL,
        ]

        while self.match(token_types):
            operator: Token = self.previous()
            right: Expr | None = self.term()

            if right:
                expr = BinaryExpr(left=expr, operator=operator, right=right)

        return expr

    def line(self) -> int:
        return self.tokens[self.current].line

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.TOKEN_TYPE_EOF

    def advance(self) -> Token:
        if not self.is_at_end():
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
        if self.is_at_end():
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
            expr: Expr | None = self.expression()

            if expr:
                self.consume(
                    TokenType.TOKEN_TYPE_RIGHT_PAREN, "Expect ') after expression."
                )
                return GroupingExpr(expression=expr)

        raise Parser.error(self.peek(), "Expect expression.")

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.TOKEN_TYPE_SEMICOLON:
                return

            match self.peek().type:
                case TokenType.TOKEN_TYPE_CLASS:
                    return
                case TokenType.TOKEN_TYPE_FUN:
                    return
                case TokenType.TOKEN_TYPE_VAR:
                    return
                case TokenType.TOKEN_TYPE_FOR:
                    return
                case TokenType.TOKEN_TYPE_IF:
                    return
                case TokenType.TOKEN_TYPE_WHILE:
                    return
                case TokenType.TOKEN_TYPE_PRINT:
                    return
                case TokenType.TOKEN_TYPE_RETURN:
                    return

            self.advance()

    def parse(self) -> Expr | None:
        try:
            return self.expression()
        except ParseError as e:
            return None
