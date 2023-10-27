from collections import defaultdict
from Transistor import Transistor


# Holds everything about netlist, every transistor inside it
class Netlist:
    def __init__(self, filename):
        self.filename = filename
        self.mosArray = {}
        self.mosTypeArray = ["", ""]  # First NMOS then PMOS
        self.in_ports = []
        self.out_ports = []
        self.nets = defaultdict(set)  # Dictionary

    def find_mos_type(self):
        with open(self.filename) as f:
            for line in f:
                tokenized = line.rstrip('\n').split(" ")
                if tokenized[0] == ".model":
                    if tokenized[2] == "NMOS":
                        self.mosTypeArray[0] = tokenized[1]
                    else:
                        self.mosTypeArray[1] = tokenized[1]

    def print_netlist(self):
        print('|{:>8}'.format("Instance name"), end=" ")
        print('|{:>8}'.format("Mos type"), end=" ")
        print('|{:>8}'.format("Width"), end=" ")
        print('|{:>8}'.format("Length"), end=" ")
        print('|{:>8}'.format("Gate node"), end=" ")
        print('|{:>8}'.format("Source node"), end=" ")
        print('|{:>8}'.format("Drain node"), end=" ")
        print('|{:>8}'.format("Bulk node"), end=" ")
        print('|{:>8}'.format("Model"), end=" ")
        print('|{:>8}'.format("Pair (if any)"), end="\n")
        for mos in self.mosArray:
            self.mosArray[mos].print_transistor()

    # Parses a SPICE netlist
    def parse(self):
        self.find_mos_type()
        with open(self.filename) as f:
            for line in f:
                tokenized = line.rstrip('\n').split(" ")
                if len(tokenized) == 8:
                    if tokenized[5] == self.mosTypeArray[0]:
                        typename = "NMOS"
                    elif tokenized[5] == self.mosTypeArray[1]:
                        typename = "PMOS"
                    mos = Transistor(name=tokenized[0], drain=tokenized[1], gate=tokenized[2],
                                     source=tokenized[3], bulk=tokenized[4], mos_model=tokenized[5],
                                     length=tokenized[6], width=tokenized[7], typename=typename)
                    self.nets[mos.drain].add(mos.instanceName + 'D')
                    self.nets[mos.gate].add(mos.instanceName + 'G')
                    self.nets[mos.source].add(mos.instanceName + 'S')
                    self.nets[mos.bulk].add(mos.instanceName + 'B')
                    self.mosArray[mos.instanceName] = mos
                elif tokenized[0] == "*>>":  # External commands
                    cmd = tokenized[1]
                    if cmd == "pairs":
                        self.mosArray[tokenized[2]].pair = self.mosArray[tokenized[3]]
                        self.mosArray[tokenized[3]].pair = self.mosArray[tokenized[2]]
                    elif cmd == "port":
                        if tokenized[2] == "input":
                            self.in_ports.append(tokenized[3])
                        else:
                            self.out_ports.append(tokenized[3])
