from parser.parser import Parser
from interpreter.token import Token, TokenType


def sample_tokens():
    tokens = []
    tokens.append(Token(type=TokenType.TOKEN_TYPE_PLUS, line=0, lexeme="+"))
    tokens.append(Token(type=TokenType.TOKEN_TYPE_MINUS, line=0, lexeme="-"))
    tokens.append(Token(type=TokenType.TOKEN_TYPE_EOF, line=0, lexeme=""))

    return tokens


def test_parser_init():
    parser = Parser(tokens=sample_tokens())

    assert parser.tokens == sample_tokens()
    assert parser.current == 0


# peek


def test_peek():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert parser.peek().type == TokenType.TOKEN_TYPE_PLUS


# previous


def test_previous():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)
    parser.advance()

    assert parser.previous().type == TokenType.TOKEN_TYPE_PLUS


# is_at_end


def test_is_at_end_when_not_at_end():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)
    assert not parser.isAtEnd()


def test_is_at_end_when_at_end():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)
    parser.advance()
    parser.advance()
    assert parser.isAtEnd()


# check


def test_check_when_diff():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert not parser.check(TokenType.TOKEN_TYPE_MINUS)


def test_check_is_eq():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert parser.check(TokenType.TOKEN_TYPE_PLUS)
