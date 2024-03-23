class Stack:
    def __init__(self):
        self.elements = []
    
    def push(self, x):
        self.elements.append(x)

    def pop(self):
        return self.elements.pop()
    
    def peek(self):
        return self.elements[-1]
    
    @property
    def empty(self):
        return (len(self.elements) > 0)