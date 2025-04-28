
import sys
import scanner

# https://craftinginterpreters.com/scanning.html#the-interpreter-framework

def run(content: str):
    print(f"will run {content}")

def run_file(filename: str):
    print(f"will run file {filename}")

    with open(filename, "r") as file:
        content = file.read()
        run(content)

def run_prompt():
    # todo
    pass

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        print(sys.argv)
        run_file(sys.argv[1])
    else:
        run_prompt()


    #if (args.length > 1) {
    #System.out.println("Usage: jlox [script]");
    #System.exit(64);
    #} else if (args.length == 1) {
    #runFile(args[0]);
    #} else {
    #runPrompt();
    #}


