import re
import operator


# Everything from netlist to LTspice schematic
class Router:
    def __init__(self, placement_file, netlist, out_file):
        self.mos_grid = []
        self.placement_file = placement_file
        self.grid_width = 0
        self.grid_height = 0
        self.asc_file = open(out_file, 'w')
        self.asc_file.write("Version 4 \nSHEET 1 900 900\n")
        self.netlist = netlist
        self.wires = []
        self.flags = []
        self.vdd_coordinate = (0, 0)
        self.gnd_coordinate = (0, 0)

    def get_grid_size(self):
        with open(self.placement_file) as f:
            file = f.readlines()
            self.grid_height = len(file)
            self.grid_width = len(re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', file[0]))
        self.mos_grid = [[None for i in range(self.grid_width)] for j in range(self.grid_height)]

    def parse_placement(self):
        self.get_grid_size()
        with open(self.placement_file) as f:
            f = f.readlines()
            for i, line in enumerate(f):
                modules = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', line.rstrip('\n'))
                for j, place in enumerate(modules):
                    if place != '()':
                        self.mos_grid[i][j] = place[1:-1]  # Chop 1st and last chars(parentheses)
                        if len(self.mos_grid[i][j].split(" ")) >= 2:
                            transistors = self.mos_grid[i][j].split(" ")
                            self.netlist.mosArray[transistors[0]].position = (i, j)
                            self.netlist.mosArray[transistors[0]].pair_left = 1
                            self.netlist.mosArray[transistors[1]].position = (i, j)
                            self.netlist.mosArray[transistors[1]].pair_left = 0
                        else:
                            self.netlist.mosArray[self.mos_grid[i][j]].position = (i, j)

    def write_mos_to_asc(self, mos):
        # Given a mos object and a pair of coordinates, this function writes it to '.asc' file appropriately.
        self.asc_file.write("SYMBOL " + ("pmos4 " if mos.typename == "PMOS" else "nmos4 ") +
                            str(mos.coordinates[1]) + " " + str(mos.coordinates[0]) + " " + str(mos.rotation) + '\n')
        self.asc_file.write("SYMATTR InstName " + mos.instanceName + '\n')
        self.asc_file.write("SYMATTR Value " + mos.model + '\n')
        self.asc_file.write("SYMATTR Value2 " + mos.length + " " + mos.width + '\n')

    def place_mos(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.mos_grid[i][j] is None:
                    continue
                if len(self.mos_grid[i][j].split(" ")) >= 2:  # pair
                    transistors = self.mos_grid[i][j].split(" ")
                    if self.netlist.mosArray[transistors[0]].rotation in ["R0", "M180"]:
                        self.netlist.mosArray[transistors[0]].coordinates = (START_Y + i * ROW_OFFSET,
                                                                             START_X + j * COL_OFFSET - int(
                                                                                 3 * PAIR_OFFSET))
                        self.netlist.mosArray[transistors[1]].coordinates = (START_Y + i * ROW_OFFSET,
                                                                             START_X + j * COL_OFFSET + int(
                                                                                 3 * PAIR_OFFSET))
                    else:
                        self.netlist.mosArray[transistors[0]].coordinates = (START_Y + i * ROW_OFFSET,
                                                                             START_X + j * COL_OFFSET - PAIR_OFFSET)
                        self.netlist.mosArray[transistors[1]].coordinates = (START_Y + i * ROW_OFFSET,
                                                                             START_X + j * COL_OFFSET + PAIR_OFFSET)
                else:
                    self.netlist.mosArray[self.mos_grid[i][j]].coordinates = (START_Y + i * ROW_OFFSET,
                                                                              START_X + j * COL_OFFSET - PAIR_OFFSET)

    def set_all_terminal_coordinates(self):
        for name, mos in self.netlist.mosArray.items():
            mos.set_terminal_coordinates()

    def rotate_mos(self):
        for name, mos in self.netlist.mosArray.items():
            if mos.source == "0" or mos.drain == "VDD":
                if mos.pair is not None:
                    self.netlist.mosArray[name].rotation = "M0" if mos.pair_left == 1 else "R0"
                else:
                    self.netlist.mosArray[name].rotation = "R0"
            elif mos.source == "VDD" or mos.drain == "0":
                if mos.pair is not None:
                    self.netlist.mosArray[name].rotation = "R180" if mos.pair_left == 1 else "M180"
                else:
                    self.netlist.mosArray[name].rotation = "R0"
            else:
                if mos.pair is not None:
                    if mos.gate == mos.pair.gate:
                        self.netlist.mosArray[name].rotation = "M0" if mos.pair_left == 1 else "R0"
                    else:
                        self.netlist.mosArray[name].rotation = "R0" if mos.pair_left == 1 else "M0"

    def append_wire_then_update(self, old_terminal, step):
        new_terminal = tuple(map(operator.sub, old_terminal, step))
        self.wires.append(Wire(old_terminal, new_terminal))
        return new_terminal

    def extend_mos_terminals(self):
        for name, mos in self.netlist.mosArray.items():
            if mos.rotation in ["R0", "M180"]:
                self.netlist.mosArray[name].gate_coordinate = self.append_wire_then_update(mos.gate_coordinate,
                                                                                           (0, EXTEND_SIZE))
                self.netlist.mosArray[name].bulk_coordinate = self.append_wire_then_update(mos.bulk_coordinate,
                                                                                           (0, -EXTEND_SIZE))
                if mos.rotation == "R0":
                    self.netlist.mosArray[name].drain_coordinate = self.append_wire_then_update(mos.drain_coordinate,
                                                                                                (EXTEND_SIZE, 0))
                    self.netlist.mosArray[name].source_coordinate = self.append_wire_then_update(mos.source_coordinate,
                                                                                                 (-EXTEND_SIZE, 0))
                else:
                    self.netlist.mosArray[name].drain_coordinate = self.append_wire_then_update(mos.drain_coordinate,
                                                                                                (-EXTEND_SIZE, 0))
                    self.netlist.mosArray[name].source_coordinate = self.append_wire_then_update(mos.source_coordinate,
                                                                                                 (EXTEND_SIZE, 0))
            elif mos.rotation in ["M0", "R180"]:
                self.netlist.mosArray[name].gate_coordinate = self.append_wire_then_update(mos.gate_coordinate,
                                                                                           (0, -EXTEND_SIZE))
                self.netlist.mosArray[name].bulk_coordinate = self.append_wire_then_update(mos.bulk_coordinate,
                                                                                           (0, EXTEND_SIZE))
                if mos.rotation == "M0":
                    self.netlist.mosArray[name].drain_coordinate = self.append_wire_then_update(mos.drain_coordinate,
                                                                                                (EXTEND_SIZE, 0))
                    self.netlist.mosArray[name].source_coordinate = self.append_wire_then_update(mos.source_coordinate,
                                                                                                 (-EXTEND_SIZE, 0))
                else:
                    self.netlist.mosArray[name].drain_coordinate = self.append_wire_then_update(mos.drain_coordinate,
                                                                                                (-EXTEND_SIZE, 0))
                    self.netlist.mosArray[name].source_coordinate = self.append_wire_then_update(mos.source_coordinate,
                                                                                                 (EXTEND_SIZE, 0))
            else:
                print("ERROR")

    def write_netlist_to_asc(self):
        for name, mos in self.netlist.mosArray.items():
            self.write_mos_to_asc(mos)

    def write_wire_to_asc(self):
        for wire in self.wires:
            self.asc_file.write(
                "WIRE " + str(wire.begin[1]) + " " + str(wire.begin[0]) + " " + str(wire.end[1]) + " " + str(
                    wire.end[0]) + "\n")

    def total_wire_cost(self):
        return sum(wire.length for wire in self.wires)

    def add_wire(self, point1, point2, lower=1):
        temp = 0, 0
        if point1[1] == point2[1] or point1[0] == point2[0]:
            self.wires.append(Wire(point1, point2))
        else:
            if (point1[0] < point2[0] and lower == 1) or (point1[0] > point2[0] and lower == 0):
                temp = point2[0], point1[1]
            elif (point1[0] > point2[0] and lower == 1) or (point1[0] < point2[0] and lower == 0):
                temp = point1[0], point2[1]
            else:
                print("WIRE ERROR")
            self.wires.append(Wire(point1, temp))
            self.wires.append(Wire(temp, point2))

    def get_coordinate(self, terminal):
        mos_terminal = terminal[-1]
        mos_name = terminal[0:-1]
        if mos_terminal == 'G':
            return self.netlist.mosArray[mos_name].gate_coordinate
        elif mos_terminal == 'D':
            return self.netlist.mosArray[mos_name].drain_coordinate
        elif mos_terminal == 'S':
            return self.netlist.mosArray[mos_name].source_coordinate
        else:
            return self.netlist.mosArray[mos_name].bulk_coordinate

    def build_mst(self, points, lower):
        num_points = len(points)
        graph = Graph(num_points)
        for i in range(num_points):
            for j in range(i + 1, num_points):
                distance = (points[i][1][1] - points[j][1][1]) ** 2 + (points[i][1][0] - points[j][1][0]) ** 2
                graph.add_edge(i, j, distance)
        edges = graph.kruskal()
        for idx, e in enumerate(sorted(edges)):
            print("Edge", points[e[0]], points[e[1]])
            point1 = points[e[0]][1]
            point2 = points[e[1]][1]
            self.add_wire(point1, point2, lower=lower)
        print("-----")

    def write_flags_to_asc(self):
        for flag in self.flags:
            self.asc_file.write("FLAG " + str(flag.point[1]) + " " + str(flag.point[0]) + " " + flag.name + '\n')

    def put_io(self):
        for io in self.netlist.in_ports + self.netlist.out_ports:
            print("Putting flag of", io)
            ins_list = list(self.netlist.nets[io])
            if len(ins_list) == 2 and io in self.netlist.out_ports:
                p0 = self.get_coordinate(ins_list[0])
                p1 = self.get_coordinate(ins_list[1])
                coordinate = (p0[0] + p1[0]) // 2, (p0[1] + p1[1]) // 2
                self.flags.append(Flag(coordinate, io))
            elif io in self.netlist.in_ports:
                for i in ins_list:
                    self.flags.append(Flag(self.get_coordinate(i), io))

    def route(self):
        flag_reg = {'0': 0, 'VDD': 0}
        for net in self.netlist.nets:
            if net in self.netlist.in_ports:
                continue
            elif not (net in ['0', 'VDD']):
                points = []
                for terminal in self.netlist.nets[net]:
                    coordinate = self.get_coordinate(terminal)
                    points.append([terminal, coordinate])
                self.build_mst(points, lower=1)
            else:
                points = []
                for terminal in sorted(self.netlist.nets[net]):
                    mos = self.netlist.mosArray[terminal[0:-1]]
                    if mos.position[0] in range(1, self.grid_height - 1):
                        self.flags.append(Flag(mos.bulk_coordinate, "0" if mos.typename == "NMOS" else "VDD"))
                    else:
                        coordinate = self.get_coordinate(terminal)
                        points.append([terminal, coordinate])
                        if flag_reg[net] == 0:
                            power_coordinate = coordinate[0] + (2 * STEP_SIZE * (1 if net == '0' else -1)), coordinate[
                                1]
                            self.flags.append(Flag(power_coordinate, net))
                            self.add_wire(power_coordinate, coordinate)
                            flag_reg[net] = 1
                self.build_mst(points, lower=(1 if net == '0' else 0))



