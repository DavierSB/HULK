class Transition:
    def __init__(self, dest_node, condition, to_write):
        self.dest_node = dest_node
        self.condition = condition
        self.to_write = to_write