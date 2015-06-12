import cell

class Library:

    def __init__(self, file):

        self.cell_arr = []

        self.generate(file)

    def generate(self, file):

        for line in file:
            self.parse(line[0:line.find('#')].lower().split())

    def parse(self, list):

        if list:
            type = list[0][(list[0].find('.')+1):]
            if type == 'cell':
                ios = self.format_ios(list[4:])
                self.cell_arr.append(cell.Cell(list[1], list[2], list[3], ios[0], ios[1]))

    def format_ios(self, list):

        ins = []
        outs = []

        for item in list:
            ins.append(item[:-2]) if (item.find('.o') == -1) else outs.append(item[:-2])

        return [ins, outs]

    def get_cell(self, id):

        for item in self.cell_arr:
            if item.get_id() == id: return item

        return False

    def __str__(self):

        string = 'LIBRARY\n'
        for cell in self.cell_arr:
            string += '\n' + str(cell)

        return string