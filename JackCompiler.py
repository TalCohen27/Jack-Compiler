import sys
from JackTokenizer import JackTokenizer
from os import listdir
from os.path import isfile, isdir, join
from CompilationEngine import CompilationEngine


def generate_code(in_file):
    tokenizer = JackTokenizer(in_file)
    tokens = tokenizer.Tokenize()
    out_file = in_file.replace('jack', 'vm')
    with open(out_file, 'w') as vm_file:
        (CompilationEngine(tokens, in_file, vm_file)).CompileClass()


if __name__ == "__main__":
    in_path = sys.argv[1]
    if isfile(in_path):
        generate_code(in_path)
    elif isdir(in_path):
        jack_files = [f for f in listdir(in_path) if isfile(join(in_path, f)) and '.jack' in f]
        for jack_file in jack_files:
            generate_code(join(in_path, jack_file))


