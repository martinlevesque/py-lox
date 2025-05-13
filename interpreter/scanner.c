#include <Python.h>
#include <string.h>

typedef enum TokenType {
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

Token scannerAddTokenLiteral(Scanner* scanner, TokenType tokenType, const char* literal) {
    char* text = substring(scanner->source, scanner->start, scanner->current);

    Token token = { .type = tokenType, .literalStr = literal, .lexeme = text, .line = scanner->line, .err = NULL };

    return token;
}

Token scannerAddToken(Scanner* scanner, TokenType tokenType) {
    return scannerAddTokenLiteral(scanner, tokenType, NULL);
}

Token scanToken(Scanner* scanner) {
    char c = scannerAdvance(scanner);

    Token t;
    t.type = TOKEN_TYPE_INVALID;

    switch (c) {
      case '(': t = scannerAddToken(scanner, TOKEN_TYPE_LEFT_PAREN); break;
      case ')': t = scannerAddToken(scanner, TOKEN_TYPE_RIGHT_PAREN); break;
      case '{': t = scannerAddToken(scanner, TOKEN_TYPE_LEFT_BRACE); break;
      case '}': t = scannerAddToken(scanner, TOKEN_TYPE_RIGHT_BRACE); break;
      case ',': t = scannerAddToken(scanner, TOKEN_TYPE_COMMA); break;
      case '.': t = scannerAddToken(scanner, TOKEN_TYPE_DOT); break;
      case '-': t = scannerAddToken(scanner, TOKEN_TYPE_MINUS); break;
      case '+': t = scannerAddToken(scanner, TOKEN_TYPE_PLUS); break;
      case ';': t = scannerAddToken(scanner, TOKEN_TYPE_SEMICOLON); break;
      case '*': t = scannerAddToken(scanner, TOKEN_TYPE_STAR); break;
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

        if (token.type == TOKEN_TYPE_INVALID) {
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

        // PyDict_SetItemString(py_token, "err", PyUnicode_FromString(t.err));
        // PyDict_SetItemString(py_token, "err", Py_None);

        PyList_SET_ITEM(py_list, i, py_token);  // steals ref to py_token

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
