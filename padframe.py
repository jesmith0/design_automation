class Padframe:

    def __init__(self, file):

        self.usable_width = -1
        self.usable_length = -1
        self.slice_width = -1
        self.slice_length = -1

        self.generate(file)

    def set_usable(self, width, length):

        self.usable_width = width
        self.usable_length = length

    def set_slice(self, width, length):

        self.slice_width = width
        self.slice_length = length

    def generate(self, file):

        for line in file:
            self.parse(line[0:line.find('#')].lower().split())

    def parse(self, list):

        if list:
            type = list[0][(list[0].find('.')+1):]
            if type == 'usable':
                self.set_usable(int(list[1]), int(list[2]))
            elif type == 'slices':
                self.set_slice(int(list[1]), int(list[2]))