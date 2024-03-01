class Action:
    def __init__(self, type, arg = None):
        self.type = type
        if self.type == 'shift':
            self.next_state = arg
            return
        if self.type == 'reduce':
            self.production = arg

    def is_shift(self):
        return self.type == 'shift'
    
    def is_reduce(self):
        return self.type == 'reduce'
    
    def is_accept(self):
        return self.type == 'accept'
    
    def is_error(self):
        return self.type == 'error'
    
    def __str__(self):
        arg = None
        if self.type == 'shift':
            arg = self.next_state
        if self.type == 'reduce':
            arg = self.production
        return self.type + " " + str(arg)
    
    def __repr__(self):
        return str(self)