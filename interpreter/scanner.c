#include <Python.h>

enum TokenType {
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
};

typedef struct {
    int type;
    const char* lexeme;
    const char* literalStr;
    unsigned char inputChar;
    size_t lineNumber;
    const char* err;  // NULL if no error
} Token;

typedef struct {
    int start;
    int current;
    int line;
    const char* source;
} Scanner;

int isAtEnd() {
}

static PyObject* scanner_scan_tokens(PyObject* self, PyObject* args) {
    const char* source;

    if (!PyArg_ParseTuple(args, "s", &source)) {
        return NULL;  // Error already set
    }

    Scanner scanner = { .start = 0, .current = 0, .line = 1, .source = source };

    // Example hardcoded array
    Token tokens[] = {
        {1, "if", "", 'i', 1, NULL},
        {2, "else", "", 'e', 1, "Unexpected token"},
    };
    int token_count = sizeof(tokens) / sizeof(Token);

    PyObject* py_list = PyList_New(token_count);

    if (!py_list) return NULL;

    for (int i = 0; i < token_count; i++) {
        Token t = tokens[i];

        PyObject* py_token = PyDict_New();

        if (!py_token) {
            Py_DECREF(py_list);
            return NULL;
        }

        PyDict_SetItemString(py_token, "type", PyLong_FromLong(t.type));
        PyDict_SetItemString(py_token, "lexeme", PyUnicode_FromString(t.lexeme));
        PyDict_SetItemString(py_token, "literalStr", PyUnicode_FromString(t.literalStr));
        PyDict_SetItemString(py_token, "inputChar", PyLong_FromUnsignedLong(t.inputChar));
        PyDict_SetItemString(py_token, "lineNumber", PyLong_FromSize_t(t.lineNumber));

        if (t.err)
            PyDict_SetItemString(py_token, "err", PyUnicode_FromString(t.err));
        else
            PyDict_SetItemString(py_token, "err", Py_None);

        PyList_SET_ITEM(py_list, i, py_token);  // steals ref to py_token
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
