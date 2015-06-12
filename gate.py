class Gate():
    
    def __init__(self, i, ins, outs):

        self.id = i
        self.inputs = ins
        self.outputs = outs
        self.d_v = 0

    def get_d_v(self):

        return self.d_v

    def set_d_v(self, val):

        self.d_v = val

    def __str__(self):

        return '\t' + str(self.id) + "\t" + str(self.inputs) + "\t" + str(self.outputs)

    def __repr__(self):

        return str(self)