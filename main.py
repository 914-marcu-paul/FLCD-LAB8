from grammar import Grammar
from parser_algorithm import ParserAlgorithm
import os


def main():
    grammar_file_path = "g1.txt"
    output_file_path = os.path.splitext(os.path.basename(grammar_file_path))[0] + ".out.txt"
    sequence_file_path = "seq.txt"
    sequence = []
    with open(sequence_file_path, 'r') as fin:
        for line in fin.readlines():
            sequence.append(line.strip())
    grammar = Grammar.from_file(grammar_file_path)
    parser_algorithm = ParserAlgorithm(grammar, sequence)
    parser_algorithm.execute(output_file_path)


if __name__ == "__main__":
    main()
