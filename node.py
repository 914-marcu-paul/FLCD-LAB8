class Node:
    def __init__(self, symbol, parent=None, left=None):
        self.symbol = symbol
        self.parent = parent
        self.left = left

    def set_parent(self, parent):
        self.parent = parent

    def set_left(self, left):
        self.left = left
