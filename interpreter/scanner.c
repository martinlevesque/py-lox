#include <Python.h>
#include <string.h>

typedef enum TokenType {
    TOKEN_TYPE_ERR,
    TOKEN_TYPE_LEFT_PAREN,
    TOKEN_TYPE_RIGHT_PAREN,
    TOKEN_TYPE_LEFT_BRACE,
    TOKEN_TYPE_RIGHT_BRACE,
    TOKEN_TYPE_LESS,
    TOKEN_TYPE_LESS_EQUAL,
    TOKEN_TYPE_GREATER,
    TOKEN_TYPE_GREATER_EQUAL,
    TOKEN_TYPE_SLASH,
    TOKEN_TYPE_SLASH_SLASH,
    TOKEN_TYPE_COMMA,
    TOKEN_TYPE_DOT,
    TOKEN_TYPE_MINUS,
    TOKEN_TYPE_PLUS,
    TOKEN_TYPE_SEMICOLON,
    TOKEN_TYPE_STAR,
    TOKEN_TYPE_EQUAL,
    TOKEN_TYPE_BANG_EQUAL,
    TOKEN_TYPE_EQUAL_EQUAL,
    TOKEN_TYPE_BANG,
    TOKEN_TYPE_SPACE,
    TOKEN_TYPE_TAB,
    TOKEN_TYPE_STRING,
    TOKEN_TYPE_NUMBER,
    TOKEN_TYPE_IDENTIFIER,
    TOKEN_TYPE_AND,
    TOKEN_TYPE_CLASS,
    TOKEN_TYPE_ELSE,
    TOKEN_TYPE_FALSE,
    TOKEN_TYPE_FOR,
    TOKEN_TYPE_FUN,
    TOKEN_TYPE_IF,
    TOKEN_TYPE_NIL,
    TOKEN_TYPE_OR,
    TOKEN_TYPE_PRINT,
    TOKEN_TYPE_RETURN,
    TOKEN_TYPE_SUPER,
    TOKEN_TYPE_THIS,
    TOKEN_TYPE_TRUE,
    TOKEN_TYPE_VAR,
    TOKEN_TYPE_WHILE,
    TOKEN_TYPE_INVALID,
    TOKEN_TYPE_NONE,
    TOKEN_TYPE_EOF
} TokenType;

typedef struct {
    int type;
    const char* lexeme;
    const char* literalStr;
    unsigned char inputChar;
    size_t line;
    const char* err;  // NULL if no error
} Token;

typedef struct {
    int start;
    int current;
    int line;
    const char* source; // raw source code
    int sourceLength;
} Scanner;

int scannerIsAtEnd(Scanner scanner) {
    return scanner.current >= scanner.sourceLength;
}

char scannerAdvance(Scanner* scanner) {
    return scanner->source[scanner->current++];
}

int scannerMatch(Scanner* scanner, char expected) {
    if (scannerIsAtEnd(*scanner)) {
        return 0;
    }

    if (scanner->source[scanner->current] != expected) {
        return 0;
    }

    ++scanner->current;

    return 1;
}

char scannerPeek(Scanner scanner) {
    if (scannerIsAtEnd(scanner)) {
        return '\0';
    }

    return scanner.source[scanner.current];
}

char scannerPeekNext(Scanner scanner) {
    if (scanner.current + 1 >= strlen(scanner.source)) {
        return '\0';
    }

    return scanner.source[scanner.current + 1];
}

void printToken(Token token) {
    printf("Token {\n");
    printf("  type: %d\n", token.type);
    printf("  lexeme: \"%s\"\n", token.lexeme ? token.lexeme : "NULL");
    printf("  literalStr: \"%s\"\n", token.literalStr ? token.literalStr : "NULL");
    printf("  inputChar: '%c'\n", token.inputChar);
    printf("  line: %zu\n", token.line);
    printf("  err: \"%s\"\n", token.err ? token.err : "NULL");
    printf("}\n");
    fflush(stdout);
}

int scannerIsDigit(char c) {
    return c >= '0' && c <= '9';
}

int scannerIsAlpha(char c) {
    return (c >= 'a' && c <= 'z') ||
           (c >= 'A' && c <= 'Z') ||
           c == '_';
}

int scannerIsAlphaNumeric(char c) {
    return scannerIsAlpha(c) || scannerIsDigit(c);
}

char* substring(const char* source, int start, int end) {
    if (start < 0 || end <= start || end > strlen(source)) {
        return NULL; // invalid indices
    }

    int length = end - start;
    char* result = (char*)malloc(length + 1); // +1 for null terminator

    if (result == NULL) {
        return NULL; // allocation failed
    }

    strncpy(result, source + start, length);
    result[length] = '\0'; // null-terminate the string

    return result;
}

Token scannerAddTokenLiteral(Scanner* scanner, TokenType tokenType, const char* literal, const char* err) {
    char* text = substring(scanner->source, scanner->start, scanner->current);

    Token token = { .type = tokenType, .literalStr = literal, .lexeme = text, .line = scanner->line, .err = err };

    return token;
}

Token scannerAddToken(Scanner* scanner, TokenType tokenType, const char* err) {
    return scannerAddTokenLiteral(scanner, tokenType, NULL, err);
}

Token readString(Scanner* scanner) {
    while (scannerPeek(*scanner) != '"' && !scannerIsAtEnd(*scanner)) {
        if (scannerPeek(*scanner) == '\n') {
            scanner->line++;
        }

        scannerAdvance(scanner);
    }

    if (scannerIsAtEnd(*scanner)) {
        return scannerAddToken(scanner, TOKEN_TYPE_ERR, "Unterminated string.");
    }

    // The closing "
    scannerAdvance(scanner);

    char* value = substring(scanner->source, scanner->start + 1, scanner->current - 1);

    return scannerAddTokenLiteral(scanner, TOKEN_TYPE_STRING, value, "");
}

Token readNumber(Scanner* scanner) {
    while (scannerIsDigit(scannerPeek(*scanner))) {
        scannerAdvance(scanner);
    }

    if (scannerPeek(*scanner) == '.' && scannerIsDigit(scannerPeekNext(*scanner))) {
        scannerAdvance(scanner);

        while (scannerIsDigit(scannerPeek(*scanner))) {
            scannerAdvance(scanner);
        }
    }

    char* textNumber = substring(scanner->source, scanner->start, scanner->current);

    return scannerAddTokenLiteral(scanner, TOKEN_TYPE_NUMBER, textNumber, "");
}

TokenType scannerDetermineTokenType(const char* identifierText) {
    if (strcmp(identifierText, "and") == 0) return TOKEN_TYPE_AND;
    if (strcmp(identifierText, "class") == 0) return TOKEN_TYPE_CLASS;
    if (strcmp(identifierText, "else") == 0) return TOKEN_TYPE_ELSE;
    if (strcmp(identifierText, "false") == 0) return TOKEN_TYPE_FALSE;
    if (strcmp(identifierText, "for") == 0) return TOKEN_TYPE_FOR;
    if (strcmp(identifierText, "fun") == 0) return TOKEN_TYPE_FUN;
    if (strcmp(identifierText, "if") == 0) return TOKEN_TYPE_IF;
    if (strcmp(identifierText, "nil") == 0) return TOKEN_TYPE_NIL;
    if (strcmp(identifierText, "or") == 0) return TOKEN_TYPE_OR;
    if (strcmp(identifierText, "print") == 0) return TOKEN_TYPE_PRINT;
    if (strcmp(identifierText, "return") == 0) return TOKEN_TYPE_RETURN;
    if (strcmp(identifierText, "super") == 0) return TOKEN_TYPE_SUPER;
    if (strcmp(identifierText, "this") == 0) return TOKEN_TYPE_THIS;
    if (strcmp(identifierText, "true") == 0) return TOKEN_TYPE_TRUE;
    if (strcmp(identifierText, "var") == 0) return TOKEN_TYPE_VAR;
    if (strcmp(identifierText, "while") == 0) return TOKEN_TYPE_WHILE;

    return TOKEN_TYPE_IDENTIFIER; // Default case
}

Token scannerIdentifier(Scanner* scanner) {
    while (scannerIsAlphaNumeric(scannerPeek(*scanner))) {
        scannerAdvance(scanner);
    }

    char* identifierText = substring(scanner->source, scanner->start, scanner->current);

    TokenType type = scannerDetermineTokenType(identifierText);
    free(identifierText);

    return scannerAddToken(scanner, type, "");
}

Token scanToken(Scanner* scanner) {
    char c = scannerAdvance(scanner);

    Token t;
    t.type = TOKEN_TYPE_INVALID;

    switch (c) {
      case '(': t = scannerAddToken(scanner, TOKEN_TYPE_LEFT_PAREN, ""); break;
      case ')': t = scannerAddToken(scanner, TOKEN_TYPE_RIGHT_PAREN, ""); break;
      case '{': t = scannerAddToken(scanner, TOKEN_TYPE_LEFT_BRACE, ""); break;
      case '}': t = scannerAddToken(scanner, TOKEN_TYPE_RIGHT_BRACE, ""); break;
      case ',': t = scannerAddToken(scanner, TOKEN_TYPE_COMMA, ""); break;
      case '.': t = scannerAddToken(scanner, TOKEN_TYPE_DOT, ""); break;
      case '-': t = scannerAddToken(scanner, TOKEN_TYPE_MINUS, ""); break;
      case '+': t = scannerAddToken(scanner, TOKEN_TYPE_PLUS, ""); break;
      case ';': t = scannerAddToken(scanner, TOKEN_TYPE_SEMICOLON, ""); break;
      case '*': t = scannerAddToken(scanner, TOKEN_TYPE_STAR, ""); break;
      case '!':
          t = scannerAddToken(scanner, scannerMatch(scanner, '=') ? TOKEN_TYPE_BANG_EQUAL : TOKEN_TYPE_BANG, "");
          break;
      case '=':
          t = scannerAddToken(scanner, scannerMatch(scanner, '=') ? TOKEN_TYPE_EQUAL_EQUAL : TOKEN_TYPE_EQUAL, "");
          break;
      case '<':
          t = scannerAddToken(scanner, scannerMatch(scanner, '=') ? TOKEN_TYPE_LESS_EQUAL : TOKEN_TYPE_LESS, "");
          break;
      case '>':
          t = scannerAddToken(scanner, scannerMatch(scanner, '=') ? TOKEN_TYPE_GREATER_EQUAL : TOKEN_TYPE_GREATER, "");
          break;
      case '/':
          if (scannerMatch(scanner, '/')) {
            while (scannerPeek(*scanner) != '\n' && ! scannerIsAtEnd(*scanner)) {
                scannerAdvance(scanner);
            }
          } else {
            t = scannerAddToken(scanner, TOKEN_TYPE_SLASH, "");
          }
          break;
      case '"':
          t = readString(scanner);

          break;
      case ' ':
      case '\r':
      case '\t':
          t.type = TOKEN_TYPE_NONE;
          break;
      case '\n':
        t.type = TOKEN_TYPE_NONE;
        scanner->line++;
        break;
      default:
        if (scannerIsDigit(c)) {
            t = readNumber(scanner);
        } else if (scannerIsAlpha(c)) {
            t = scannerIdentifier(scanner);
        } else {
            t = scannerAddToken(scanner, TOKEN_TYPE_ERR, "Unexpected character.");
        }
        break;
    }

    return t;
}

void freeToken(Token token) {
    if (token.lexeme != NULL) {
        free(token.lexeme);
    }

    if (token.literalStr != NULL) {
        free(token.literalStr);
    }
}

static PyObject* scanner_scan_tokens(PyObject* self, PyObject* args) {
    Scanner scanner = { .start = 0, .current = 0, .line = 1 };

    if (!PyArg_ParseTuple(args, "s", &scanner.source)) {
        return NULL;  // Error already set
    }
    scanner.sourceLength = strlen(scanner.source);

    // Example hardcoded array
    int token_count = scanner.sourceLength * 2;

    PyObject* py_list = PyList_New(token_count);

    if (!py_list) return NULL;

    int i = 0;

    while (!scannerIsAtEnd(scanner)) {
        scanner.start = scanner.current;

        Token token = scanToken(&scanner);

        if (token.type == TOKEN_TYPE_INVALID || token.type == TOKEN_TYPE_NONE) {
            continue;
        }

        PyObject* py_token = PyDict_New();

        if (!py_token) {
            Py_DECREF(py_list);
            return NULL;
        }

        PyDict_SetItemString(py_token, "type", PyLong_FromLong(token.type));
        PyDict_SetItemString(py_token, "lexeme", token.lexeme ? PyUnicode_FromString(token.lexeme) : Py_None);
        PyDict_SetItemString(py_token, "literalStr", token.literalStr ? PyUnicode_FromString(token.literalStr) : Py_None);
        PyDict_SetItemString(py_token, "inputChar", PyLong_FromUnsignedLong(token.inputChar));
        PyDict_SetItemString(py_token, "line", PyLong_FromSize_t(token.line));

        PyDict_SetItemString(py_token, "err", PyUnicode_FromString(token.err));

        PyList_SET_ITEM(py_list, i, py_token);

        ++i;

        freeToken(token);
    }

    if (i < token_count) {
        if (PyList_SetSlice(py_list, i, token_count, NULL) < 0) {
            Py_DECREF(py_list);
            return NULL;
        }
    }

    return py_list;
}

// Method definitions
static PyMethodDef MyModuleMethods[] = {
    {"scan_tokens", scanner_scan_tokens, METH_VARARGS, "Add two integers"},
    {NULL, NULL, 0, NULL}
};

// Module definition (Python 3)
static struct PyModuleDef mymodule_definition = {
    PyModuleDef_HEAD_INIT,
    "scanner",        // name of module
    "A simple example module",  // module docstring
    -1,                // size of per-interpreter state of the module, -1 means global
    MyModuleMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_scanner(void) {
    return PyModule_Create(&mymodule_definition);
}
