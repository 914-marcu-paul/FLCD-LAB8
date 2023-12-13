import copy
from queue import Queue
from node import Node
from parsing_strategy import ParserStrategy
from parsing_configuration import ParsingConfiguration
from parsing_state import ParsingState


class ParserAlgorithm:
    def __init__(self, grammar, sequence):
        self.grammar = grammar
        self.initial_configuration = ParsingConfiguration(beta=[grammar.get_start_symbol()])
        self.strategy = ParserStrategy(grammar.production_rules.copy())
        self.sequence = sequence

    def execute(self, output_file_path):
        config = self.execute_algorithm()

        if config.s == ParsingState.FINAL:
            output = self.get_table_from_config(config)
        else:
            output = "ERROR"

        print(output)
        with open(output_file_path, 'w') as file:
            file.write(output)

    def execute_algorithm(self):
        config = copy.deepcopy(self.initial_configuration)
        step = 1

        while config.s != ParsingState.FINAL and config.s != ParsingState.ERROR:
            print(f"{step}: {config} ", end="")
            if config.s == ParsingState.NORMAL:
                if config.i == len(self.sequence) + 1 and not config.beta:
                    # SUCCESS
                    print("SUCCESS")
                    self.strategy.success(config)
                    config = config.next
                else:
                    if config.beta and self.grammar.is_non_terminal_symbol(config.beta[-1]):
                        # EXPAND
                        print("EXPAND")
                        self.strategy.expand(config)
                        config = config.next
                    elif config.i - 1 < len(self.sequence) and config.beta and \
                            config.beta[-1] == self.sequence[config.i - 1]:
                        # ADVANCE
                        print("ADVANCE")
                        self.strategy.advance(config)
                        config = config.next
                    else:
                        # MOMENTARY INSUCCESS
                        print("MOMENTARY INSUCCESS")
                        self.strategy.momentary_insuccess(config)
                        config = config.next
            elif config.s == ParsingState.BACK:
                if self.grammar.is_terminal_symbol(config.alpha[-1]):
                    # BACK
                    print("BACK")
                    self.strategy.back(config)
                    config = config.next
                else:
                    # ANOTHER TRY
                    print("ANOTHER TRY")
                    self.strategy.another_try(config)
                    config = config.next

            step += 1

        print(config)
        return config

    def get_table_from_config(self, config):
        sb = [f"Sequence: {self.sequence}\n"]

        for row in self.config_to_table(config):
            sb.append("{:<10} {:<10} {:<10} {:<10}\n".format(row[0], row[1], row[2], row[3]))

        return ''.join(sb)

    def config_to_table(self, config):
        return self.tree_to_table(self.alpha_to_tree(self.get_alpha_from_config(config)))

    def get_alpha_from_config(self, config):
        alpha = []
        for entry in reversed(config.alpha_to_list_of_productions_string()):
            symbol, number = entry
            if self.grammar.is_non_terminal(symbol):
                production_rule_rhs = self.grammar.get_lhs_of_ith_production_rule_of_symbol(symbol, number)
                alpha.append((symbol, production_rule_rhs))
        return alpha

    def alpha_to_tree(self, alpha):
        lhs = alpha[-1][0]

        tree = []
        root = Node(lhs)
        tree.append(root)
        queue = Queue()
        queue.put(root)

        while not queue.empty():
            current_node = queue.get()
            production_rule_rhs = alpha.pop()[1]

            for i in range(len(production_rule_rhs)):
                rhs_element = production_rule_rhs[i]

                child = Node(rhs_element, current_node)
                if i != 0:
                    child.left = tree[-1]
                tree.append(child)
                if self.grammar.is_non_terminal_symbol(rhs_element):
                    queue.put(child)

        return tree

    @staticmethod
    def tree_to_table(tree):
        table = [["index", "info", "parent", "right sibling"]]

        for i, node in enumerate(tree):
            row = [str(i + 1), node.symbol, str(tree.index(node.parent) + 1) if node.parent else "-",
                   str(tree.index(node.left) + 1) if node.left else "-"]
            table.append(row)

        return table

    '''
    from what I understand, alpha is the thing that matters, meaning that it is the answer to g3
    S[1] a S[2] a S[3] c b S[3] c
    1 - a S b S
    2 - a S
    3 - c
    
    the tree should look like this
               S
    a      S       b       S
         a   S             c
             c
             
    config.alpha = ['S', 'a', 'S', 'a', 'S', 'c', 'b', 'S', 'c']
    config.index_mapping = OrderedDict([(0, 1), (2, 2), (4, 3), (7, 3)])
    self.strategy.production_rules = {'S': [('a S b S', 1), ('a S', 2), ('c', 3)]}
    '''
