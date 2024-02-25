import queue

class Stack:
    def __init__(self):
        self.__stack = queue.LifoQueue()
    
    def push(self, x):
        self.__stack.put(x)

    def pop(self):
        return self.__stack.get()
    
    def peek(self):
        return self.__stack[-1]