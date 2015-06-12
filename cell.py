class Cell:

    def __init__(self, i, ws, ls, in_arr, out_arr):

        self.id = i
        self.width_size = ws
        self.length_size = ls
        self.ins = in_arr
        self.out = out_arr
        self.in_width = len(in_arr)
        self.out_width = len(out_arr)

    def get_id(self):

        return str(self.id)

    def __str__(self):

        string = ''
        string += str(self.id) + '\t'
        string += str(self.width_size) + '\t'
        string += str(self.length_size) + '\t'
        string += str(self.ins) + '\t'
        string += str(self.out) + '\t'
        string += str(self.in_width) + '\t'
        string += str(self.out_width) + '\t'

        return string