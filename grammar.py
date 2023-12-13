class Grammar:
    EPSILON = "E"

    def __init__(self, non_terminal_symbols, terminal_symbols, production_rules, start_symbol):
        self.non_terminal_symbols = non_terminal_symbols
        self.terminal_symbols = terminal_symbols
        self.production_rules = production_rules
        self.start_symbol = start_symbol

    def get_start_symbol(self):
        return self.start_symbol

    def is_terminal_symbol(self, symbol):
        if symbol in self.terminal_symbols:
            return True
        return False

    def is_non_terminal_symbol(self, symbol):
        if symbol in self.non_terminal_symbols:
            return True
        return False

    @staticmethod
    def validate(non_terminal_symbols, terminal_symbols, production_rules, start_symbol):
        if start_symbol not in non_terminal_symbols:
            return False
        for key in production_rules.keys():
            if key not in non_terminal_symbols:
                return False
            for move in production_rules[key]:
                for char in move:
                    if char not in non_terminal_symbols and char not in terminal_symbols and char != 'E':
                        return False
        return True

    @staticmethod
    def parse_line(line):
        return [value.strip() for value in line[3:].strip()[1:-1].strip().split(',')]

    @staticmethod
    def from_file(file_name):
        with open(file_name, 'r') as file:
            non_terminal_symbols = Grammar.parse_line(file.readline())
            terminal_symbols = Grammar.parse_line(file.readline())
            start_symbol = file.readline().split('=')[1].strip()
            production_rules = Grammar.parse_rules(Grammar.parse_line(''.join([line for line in file])))
            return Grammar(non_terminal_symbols, terminal_symbols, production_rules, start_symbol)

    @staticmethod
    def parse_rules(rules):
        result = {}
        index = 1

        for rule in rules:
            left_side, right_side = rule.split('->')
            left_side = left_side.strip()
            right_side = [value.strip() for value in right_side.split('|')]
            for value in right_side:
                if left_side in result.keys():
                    result[left_side].append((value, index))
                else:
                    result[left_side] = [(value, index)]
                index += 1
        return result

    @staticmethod
    def split_right_side(prod):
        return prod.split(' ')

    def is_non_terminal(self, value):
        return value in self.non_terminal_symbols

    def is_terminal(self, value):
        return value in self.terminal_symbols

    def get_production_rules_for(self, non_terminal):
        if not self.is_non_terminal(non_terminal):
            raise Exception('Can only show productions for non-terminals')
        for key in self.production_rules.keys():
            if key == non_terminal:
                return self.production_rules[key]

    def get_production_rule_for_index(self, index):
        for key, value in self.production_rules.items():
            for v in value:
                if v[1] == index:
                    return key, v[0]

    def get_lhs_of_ith_production_rule_of_symbol(self, symbol, i):
        production_rules_of_symbol_with_spaces = self.production_rules[symbol][i-1][0]
        production_rules_of_symbol = []
        for prod in production_rules_of_symbol_with_spaces:
            if prod != " ":
                production_rules_of_symbol.append(prod)
        return list(list(production_rules_of_symbol))

    def get_production_rule_as_str(self):
        result_string = ""
        for key, values in self.production_rules.items():
            result_string += str(key) + " -> "
            for value in values:
                result_string += str(value) + ", "
            result_string = result_string[:-2]
            result_string += '\n'
        return result_string

    def check_cfg(self):
        has_starting_symbol = False
        for key in self.production_rules.keys():
            if key == self.start_symbol:
                has_starting_symbol = True
            if key not in self.non_terminal_symbols:
                return False
        if not has_starting_symbol:
            return False
        for production in self.production_rules.values():
            for rhs in production:
                index = 0
                while index < len(rhs) - 1:
                    values = rhs[index]
                    split_values = values.split(' ')
                    for value in split_values:
                        if value not in self.non_terminal_symbols and value not in self.terminal_symbols \
                                and value != Grammar.EPSILON:
                            return False
                    index += 1
        return True

    def print_syntax(self):
        return 'non_terminal_symbols = { ' + ', '.join(self.non_terminal_symbols) + ' }\n' \
               + 'terminal_symbols = { ' + ', '.join(self.terminal_symbols) + ' }\n' \
               + 'production_rules = { ' + '\n' + self.get_production_rule_as_str() + '}\n' \
               + 'start_symbol = ' + str(self.start_symbol) + '\n' \
               + 'is cfg? ' + str(self.check_cfg()) + '\n'
