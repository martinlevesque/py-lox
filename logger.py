import sys


def out(content: str):
    print(content, end="", flush=True)


def err(content: str):
    print(content, file=sys.stderr, end="", flush=True)


def fatal(content: str):
    print(content, file=sys.stderr, end="", flush=True)
    sys.exit(1)
