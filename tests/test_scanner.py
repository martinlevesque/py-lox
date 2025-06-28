from interpreter.token import TokenType
import scanner


def test_scanner_simple_operators():
    result = scanner.scan_tokens("+-")
    assert len(result) == 2
    assert TokenType(result[0]["type"]) == TokenType.TOKEN_TYPE_PLUS
    assert result[0]["lexeme"] == "+"
    assert result[0]["err"] == ""

    assert TokenType(result[1]["type"]) == TokenType.TOKEN_TYPE_MINUS
    assert result[1]["lexeme"] == "-"
    assert result[1]["err"] == ""


def test_scanner_number():
    result = scanner.scan_tokens("1234.34")
    assert len(result) == 1
    assert TokenType(result[0]["type"]) == TokenType.TOKEN_TYPE_NUMBER
    assert result[0]["lexeme"] == "1234.34"
    assert result[0]["err"] == ""
