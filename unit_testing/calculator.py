class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def do_sum(self):
        return self.a + self.b
    
    def do_minus(self):
        return self.a - self.b
    
    def do_multiply(self):
        return self.a * self.b
    
    def do_divide(self):
        return self.a / self.b