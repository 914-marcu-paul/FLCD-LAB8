from collections import OrderedDict
from parsing_state import ParsingState


class ParsingConfiguration:
    def __init__(self, s=ParsingState.NORMAL, i=1, alpha=None, index_mapping=None, beta=None):
        self.s = s
        self.i = i
        self.alpha = alpha or []
        self.index_mapping = index_mapping or OrderedDict()
        self.beta = beta or []
        self.next = None

    def __str__(self):
        alpha_string = ""
        index = 0
        for symbol in self.alpha:
            alpha_string += symbol
            if index in self.index_mapping:
                alpha_string += "[" + str(self.index_mapping[index]) + "]"
            if index < len(self.alpha) - 1:
                alpha_string += " "
            index += 1

        beta_string = " ".join(self.beta)
        result_string = "({}, {}, {}, {})".format(str(self.s), str(self.i), alpha_string, beta_string)
        return result_string

    def alpha_to_list_of_productions_string(self):
        alpha_list = []
        index = 0
        for symbol in self.alpha:
            if index in self.index_mapping.keys():
                local_rule_number = self.index_mapping[index]
                alpha_list.append((symbol, local_rule_number))
            index += 1
        return alpha_list
