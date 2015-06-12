import padframe, library, netlist

# TODO: add option to specify input file path/name

f_pad = open('padframe.lib', 'r')
pad = padframe.Padframe(f_pad)
f_pad.close()

f_lib = open('library.lib', 'r')
lib = library.Library(f_lib)
f_lib.close()

f_net = open('C17.netblif', 'r')
net = netlist.Netlist(f_net, pad, lib)
f_net.close()

# KERNIGHAN-LIN 2-WAY PARTITIONING

def get_connectivity(key, part, internal):

    count = 0
    for comp_wire in (key.inputs + key.outputs):
        for gate in part:
            for wire in (gate.inputs + gate.outputs):
                if comp_wire == wire:
                    count += 1

    if (internal): return count - len(key.inputs + key.outputs)
    else: return count # returns number of connections for gate within/across partitions

def update_dv(part):

    for gate in part[0]:

        int = get_connectivity(gate, part[0], True) # internal
        ext = get_connectivity(gate, part[1], False) # external
        gate.set_d_v(ext - int)

    for gate in part[1]:

        int = get_connectivity(gate, part[1], True) # internal
        ext = get_connectivity(gate, part[0], False) # external
        gate.set_d_v(ext - int) # updates d_v value of Gate objects

def get_max_part_sum(queue):

    k = -1
    max = float('-inf')

    i = 1
    tot = 0

    for step in queue:
        tot += step[2]
        if (tot > max):
            max = tot
            if (max > 0):
                k = i
        i += 1

    return k # returns k to maximize partial sum, -1 if G <= 0 (algorithm done)

def update_part(netlist, queue, k):

    for i in range(k):

        netlist.remove(queue[i][0], 0)
        netlist.remove(queue[i][1], 1)
        netlist.append(queue[i][1], 0)
        netlist.append(queue[i][0], 1)

    INIT_PART = netlist.get_part()

# STEP 1:
# initial partition = |A| = |B| = |V|/2
INIT_PART = [net.get_gates()[:len(net.get_gates())/2], net.get_gates()[len(net.get_gates())/2:]]
done = False

# create a deep copy of partition for netlist data structure
net.set_part(INIT_PART)

while (not done): # while partial sum postive

    # STEP 2:
    # compute D_v, set initials
    part = net.get_part()   # V' = V
    queue = []              # improvements
    it = 0                  # interations

    while (part[0] and part[1]): # while both partitions contain gates (STEP 4)

        # compute D_v for all V'
        it += 1
        update_dv(part)

        # STEP 3:
        # maximize g_i, update queue & partition

        max_g_i = float("-inf")

        for gate_a in part[0]:
            for gate_b in part[1]:

                if len(set(gate_a.inputs + gate_a.outputs).intersection(gate_b.inputs + gate_b.outputs)) > 0: c = 1
                else: c = 0
        
                g_i = (gate_a.get_d_v() + gate_b.get_d_v()) - (2*c)
                if (g_i > max_g_i):
                    max_g_i = g_i
                    a_i = gate_a
                    b_i = gate_b

        queue.append([a_i, b_i, max_g_i])

        part[0].remove(a_i)
        part[1].remove(b_i)

        # STEP 4:
        # loop until A' or B' empty

    # STEP 5:
    # calculate partial sum, update partition, loop
    k = get_max_part_sum(queue)

    if (k == -1):
        done = True
    else:
        update_part(net, queue, k)

# DISPLAY PARTITION

part = net.get_part()

print '\nPARTITION A'
for gate in part[0]:
    print gate
print

print 'PARTITION B'
for gate in part[1]:
    print gate
print