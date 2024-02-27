class Action:
    def __init__(self, type, arg):
        self.type = type
        if self.type == 'reduce':
            self.next_state = arg
            return
        if self.type == 'shift':
            self.production = arg

    def is_shift(self):
        return self.type == 'shift'
    
    def is_reduce(self):
        return self.type == 'reduce'
    
    def is_accept(self):
        return self.type == 'accept'
    
    def is_error(self):
        return self.type == 'error'