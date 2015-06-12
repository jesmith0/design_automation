import gate, copy

class Netlist:

    def __init__(self, file, pad, lib):

        self.id = ''
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.gates = []

        self.padframe = pad
        self.library = lib

        self.partition = []

        self.generate(file)

    def generate(self, file):

        for line in file:
            self.parse(line[0:line.find('#')].lower().split())

    def parse(self, list):

        if list:
            type = list[0][(list[0].find('.')+1):]
            if type == 'model':
                self.id = list[1]
            elif type == 'inputs':
                self.inputs = list[1:]
            elif type == 'outputs':
                self.outputs = list[1:]
            elif type == 'gate':
                self.add_gate(list[1:])
            elif type == 'end':
                return True

    def set_part(self, part):

        self.partition = copy.deepcopy(part)

    def get_part(self):

        return copy.deepcopy(self.partition)

    def get_gates(self):

        return self.gates

    def add_gate(self, list):

        cell = self.library.get_cell(list[0])
        if (cell != False):

            ins = []
            outs = []

            for x in range(cell.in_width):
                wire = list[x + 1][list[x + 1].find('=') + 1:]
                if not ((wire in self.inputs) or (wire in self.outputs) or (wire in self.wires)): self.wires.append(wire)
                ins.append(wire)

            for y in range(cell.out_width):
                wire = list[cell.in_width + y + 1][list[cell.in_width + y + 1].find('=') + 1:] # wow great python
                if not ((wire in self.inputs) or (wire in self.outputs) or (wire in self.wires)): self.wires.append(wire)
                outs.append(wire)

            self.gates.append(gate.Gate(list[0], ins, outs))

        else:
            print "\n" + str(list[0]) + " DOES NOT EXIST\n"
            return False

    def remove(self, gate, part):

        # remove and equivalent gate from a given partition
        for item in self.partition[part]:
            if ((gate.id == item.id) and (set(gate.inputs) == set(item.inputs)) and (set(gate.outputs) == set(item.outputs))):
                self.partition[part].remove(item)
                return 1

    def append(self, gate, part):

        self.partition[part].append(gate)

    def __str__(self):

        gates_str = ''
        for item in self.gates:
            gates_str += str(item) + '\n'

        string = ''
        string += 'MODEL:\t' + str(self.id) + '\n'
        string += '\nINPUTS:\t' + str(self.inputs) + '\n'
        string += '\nOUTPUTS:\t' + str(self.outputs) + '\n'
        string += '\nWIRES:\t' + str(self.wires) + '\n'
        string += '\nGATES:' + gates_str + '\n'

        return str(self.padframe) + '\n\n' + str(self.library) + '\n\n' + string