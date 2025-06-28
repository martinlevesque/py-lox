from dataclasses import dataclass
from enum import IntEnum, auto


class AutoEnum(IntEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return count  # count starts at 0


class TokenType(AutoEnum):
    TOKEN_TYPE_ERR = auto()
    TOKEN_TYPE_LEFT_PAREN = auto()
    TOKEN_TYPE_RIGHT_PAREN = auto()
    TOKEN_TYPE_LEFT_BRACE = auto()
    TOKEN_TYPE_RIGHT_BRACE = auto()
    TOKEN_TYPE_LESS = auto()
    TOKEN_TYPE_LESS_EQUAL = auto()
    TOKEN_TYPE_GREATER = auto()
    TOKEN_TYPE_GREATER_EQUAL = auto()
    TOKEN_TYPE_SLASH = auto()
    TOKEN_TYPE_SLASH_SLASH = auto()
    TOKEN_TYPE_COMMA = auto()
    TOKEN_TYPE_DOT = auto()
    TOKEN_TYPE_MINUS = auto()
    TOKEN_TYPE_PLUS = auto()
    TOKEN_TYPE_SEMICOLON = auto()
    TOKEN_TYPE_STAR = auto()
    TOKEN_TYPE_EQUAL = auto()
    TOKEN_TYPE_BANG_EQUAL = auto()
    TOKEN_TYPE_EQUAL_EQUAL = auto()
    TOKEN_TYPE_BANG = auto()
    TOKEN_TYPE_SPACE = auto()
    TOKEN_TYPE_TAB = auto()
    TOKEN_TYPE_STRING = auto()
    TOKEN_TYPE_NUMBER = auto()
    TOKEN_TYPE_IDENTIFIER = auto()
    TOKEN_TYPE_AND = auto()
    TOKEN_TYPE_CLASS = auto()
    TOKEN_TYPE_ELSE = auto()
    TOKEN_TYPE_FALSE = auto()
    TOKEN_TYPE_FOR = auto()
    TOKEN_TYPE_FUN = auto()
    TOKEN_TYPE_IF = auto()
    TOKEN_TYPE_NIL = auto()
    TOKEN_TYPE_OR = auto()
    TOKEN_TYPE_PRINT = auto()
    TOKEN_TYPE_RETURN = auto()
    TOKEN_TYPE_SUPER = auto()
    TOKEN_TYPE_THIS = auto()
    TOKEN_TYPE_TRUE = auto()
    TOKEN_TYPE_VAR = auto()
    TOKEN_TYPE_WHILE = auto()
    TOKEN_TYPE_INVALID = auto()
    TOKEN_TYPE_NONE = auto()
    TOKEN_TYPE_EOF = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    literal: str | None = None


def load_token(hash_input: dict) -> Token:
    return Token(
        type=TokenType(hash_input["type"]),
        lexeme=hash_input["lexeme"],
        line=hash_input["line"],
        literal=hash_input["literalStr"],
    )
