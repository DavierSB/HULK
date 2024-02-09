class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line
    
    def __str__(self):
        return "( " + self.type + "   " + str(self.value) + "   in line " + str(self.line) + " )"