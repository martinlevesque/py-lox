from parser.parser import Parser
from interpreter.token import Token, TokenType


def sample_tokens():
    tokens = []
    tokens.append(Token(type=TokenType.TOKEN_TYPE_PLUS, line=0, lexeme="+"))
    tokens.append(Token(type=TokenType.TOKEN_TYPE_MINUS, line=0, lexeme="-"))

    return tokens


def test_parser_init():
    parser = Parser(tokens=sample_tokens())

    assert parser.tokens == sample_tokens()
    assert parser.current == 0


def test_peek():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert parser.peek().type == TokenType.TOKEN_TYPE_PLUS


def test_previous():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)
    parser.current += 1

    assert parser.previous().type == TokenType.TOKEN_TYPE_PLUS
