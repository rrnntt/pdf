import string_parser as sp

class Operators:
    """
    Operators used in an expression.
    
    Args:
        binary (list[str]): 
    """
    def __init__(self, binary):
        self.binary = binary
        self.precedence = {}
        self.op_chars = ''
        prec = 1
        for op_str in self.binary:
            ops = op_str.split(' ')
            

class OpListParser(sp.Parser):
    def __init__(self):
        sp.Parser.__init__(self)
        
