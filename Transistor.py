# Transistor class to store everything about transistors in netlist
class Transistor:
    def __init__(self, name, drain, gate, source, bulk, mos_model, length, width, typename):
        # Everything is string
        self.width = width
        self.length = length
        self.gate = gate
        self.source = source
        self.drain = drain
        self.bulk = bulk
        self.model = mos_model  # Depends on the library
        self.instanceName = name  # M1, M2 ...
        self.coordinates = (0, 0)  # Center point
        self.rotation = "R0"  # R0, R90, R180, R270
        self.typename = typename  # NMOS or PMOS
        self.pair = None  # Mos object
        self.pair_left = 0
        self.position = (0, 0)
        self.drain_coordinate = (0, 0)
        self.bulk_coordinate = (0, 0)
        self.gate_coordinate = (0, 0)
        self.source_coordinate = (0, 0)

    def set_terminal_coordinates(self):
        if self.rotation == "R0":
            self.bulk_coordinate = self.coordinates[0] + 48, self.coordinates[1] + 48
            self.gate_coordinate = self.coordinates[0] + 80, self.coordinates[1] + 0
            self.source_coordinate = self.coordinates[0] + 96, self.coordinates[1] + 48
            self.drain_coordinate = self.coordinates[0] + 0, self.coordinates[1] + 48
        elif self.rotation == "M0":
            self.bulk_coordinate = self.coordinates[0] + 48, self.coordinates[1] - 48
            self.gate_coordinate = self.coordinates[0] + 80, self.coordinates[1] - 0
            self.source_coordinate = self.coordinates[0] + 96, self.coordinates[1] - 48
            self.drain_coordinate = self.coordinates[0] + 0, self.coordinates[1] - 48
        elif self.rotation == "M180":
            self.bulk_coordinate = self.coordinates[0] + 48, self.coordinates[1] + 48
            self.gate_coordinate = self.coordinates[0] + 80, self.coordinates[1] - 0
            self.source_coordinate = self.coordinates[0] + 0, self.coordinates[1] + 48
            self.drain_coordinate = self.coordinates[0] + 96, self.coordinates[1] + 48
        elif self.rotation == "R180":
            self.bulk_coordinate = self.coordinates[0] + 48, self.coordinates[1] - 48
            self.gate_coordinate = self.coordinates[0] + 80, self.coordinates[1] - 0
            self.source_coordinate = self.coordinates[0] + 0, self.coordinates[1] - 48
            self.drain_coordinate = self.coordinates[0] + 96, self.coordinates[1] - 48
        else:
            print("TERMINAL_ERROR " + self.rotation)

    def print_transistor(self):
        print('|{:>8}'.format(self.instanceName), end=" ")
        print('|{:>12}'.format(self.typename), end=" ")
        print('|{:>9}'.format(self.width), end=" ")
        print('|{:>8}'.format(self.length), end=" ")
        print('|{:>8}'.format(self.gate), end=" ")
        print('|{:>8}'.format(self.source), end=" ")
        print('|{:>10}'.format(self.drain), end=" ")
        print('|{:>10}'.format(self.bulk), end=" ")
        print('|{:>10}'.format(self.model), end=" ")
        print('|{:>8}'.format("None" if self.pair is None else self.pair.instanceName), end="\n")

