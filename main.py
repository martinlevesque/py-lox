import sys
import scanner
import logger

# https://craftinginterpreters.com/scanning.html#error-handling


def run(content: str):
    tokens: list = scanner.scan_tokens(content)

    if not tokens:
        logger.fatal(f"no token received, content={content}")

    for token in tokens:
        logger.out(f"{token}\n")


def run_file(filename: str):
    with open(filename, "r") as file:
        content = file.read()
        run(content)


def run_prompt():
    # todo
    while True:
        logger.out("> ")
        line = sys.stdin.readline()
        run(line)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        logger.out("Usage: plox [script]\n")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()
