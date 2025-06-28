from parser.parser import Parser, ParseError
from interpreter.token import Token, TokenType
from syntax_tree.ast_printer import AstPrinter
from syntax_tree.unary_expr import UnaryExpr
from syntax_tree.literal_expr import LiteralExpr
import pytest


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


def test_parser_peek():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert parser.peek().type == TokenType.TOKEN_TYPE_PLUS


# previous


def test_parser_previous():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)
    parser.advance()

    assert parser.previous().type == TokenType.TOKEN_TYPE_PLUS


# is_at_end


def test_parser_is_at_end_when_not_at_end():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)
    assert not parser.is_at_end()


def test_parser_is_at_end_when_at_end():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)
    parser.advance()
    parser.advance()
    assert parser.is_at_end()


# check


def test_parser_check_when_diff():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert not parser.check(TokenType.TOKEN_TYPE_MINUS)


def test_parser_check_is_eq():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert parser.check(TokenType.TOKEN_TYPE_PLUS)


# match


def test_parser_match_is_currently_type():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert parser.match([TokenType.TOKEN_TYPE_PLUS])
    assert parser.current == 1


def test_parser_match_is_not_currently_type():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    assert not parser.match([TokenType.TOKEN_TYPE_MINUS])
    assert parser.current == 0


# primary


def test_parser_primary_when_false():
    tokens = []
    tokens.append(Token(type=TokenType.TOKEN_TYPE_FALSE, line=1, lexeme="false"))
    parser = Parser(tokens=tokens)

    result = parser.primary()

    if not result:
        assert False

    assert type(result) == LiteralExpr
    assert result.literal.type == TokenType.TOKEN_TYPE_FALSE


def test_parser_primary_when_true():
    tokens = []
    tokens.append(Token(type=TokenType.TOKEN_TYPE_TRUE, line=1, lexeme="true"))
    parser = Parser(tokens=tokens)

    result = parser.primary()

    if not result:
        assert False

    assert type(result) == LiteralExpr
    assert result.literal.type == TokenType.TOKEN_TYPE_TRUE


def test_parser_primary_when_nil():
    tokens = []
    tokens.append(Token(type=TokenType.TOKEN_TYPE_NIL, line=1, lexeme="nil"))
    parser = Parser(tokens=tokens)

    result = parser.primary()

    if not result:
        assert False

    assert type(result) == LiteralExpr
    assert result.literal.type == TokenType.TOKEN_TYPE_NIL


def test_parser_primary_when_number():
    tokens = []
    tokens.append(
        Token(type=TokenType.TOKEN_TYPE_NUMBER, line=1, lexeme="45.6", literal="45.6")
    )
    parser = Parser(tokens=tokens)

    result = parser.primary()

    if not result:
        assert False

    assert type(result) == LiteralExpr
    assert result.literal.type == TokenType.TOKEN_TYPE_NUMBER
    assert result.literal.literal == "45.6"


def test_parser_primary_when_string():
    tokens = []
    tokens.append(
        Token(
            type=TokenType.TOKEN_TYPE_STRING, line=1, lexeme='"hello"', literal="hello"
        )
    )
    parser = Parser(tokens=tokens)

    result = parser.primary()

    if not result:
        assert False

    assert type(result) == LiteralExpr
    assert result.literal.type == TokenType.TOKEN_TYPE_STRING
    assert result.literal.literal == "hello"


# consume


def test_parser_consume_happy_path():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    result: Token = parser.consume(TokenType.TOKEN_TYPE_PLUS, "expecting plus")

    assert result.type == TokenType.TOKEN_TYPE_PLUS


def test_parser_consume_diff_token():
    tokens = sample_tokens()
    parser = Parser(tokens=tokens)

    with pytest.raises(ParseError):
        parser.consume(TokenType.TOKEN_TYPE_EOF, "invalid")


# parse


def test_parser_parse_simple_literal():
    tokens = []
    tokens.append(
        Token(type=TokenType.TOKEN_TYPE_NUMBER, line=1, lexeme="55", literal="55")
    )
    tokens.append(Token(type=TokenType.TOKEN_TYPE_EOF, line=1, lexeme=""))

    parser = Parser(tokens=tokens)

    result = parser.parse()

    assert result is not None
    assert type(result) == LiteralExpr
    assert result.literal.type == TokenType.TOKEN_TYPE_NUMBER
    assert result.literal.literal == "55"


def test_parser_parse_unary_group():
    # -(10 + 5)
    tokens = []
    tokens.append(Token(type=TokenType.TOKEN_TYPE_MINUS, line=1, lexeme="-"))
    tokens.append(
        Token(type=TokenType.TOKEN_TYPE_LEFT_PAREN, line=1, lexeme="", literal="")
    )
    tokens.append(
        Token(type=TokenType.TOKEN_TYPE_NUMBER, line=1, lexeme="10", literal="10")
    )
    tokens.append(Token(type=TokenType.TOKEN_TYPE_PLUS, line=1, lexeme="+"))
    tokens.append(
        Token(type=TokenType.TOKEN_TYPE_NUMBER, line=1, lexeme="5", literal="5")
    )
    tokens.append(
        Token(type=TokenType.TOKEN_TYPE_RIGHT_PAREN, line=1, lexeme="", literal="")
    )
    tokens.append(Token(type=TokenType.TOKEN_TYPE_EOF, line=1, lexeme=""))

    parser = Parser(tokens=tokens)

    result = parser.parse()

    assert result is not None
    assert type(result) == UnaryExpr

    ast_printer = AstPrinter()
    ast_str = ast_printer.print(result)

    assert ast_str == "(- (group (+ 10 5)))"
