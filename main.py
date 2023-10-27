from Netlist import  Netlist
from Router import *

# Parameters for schematic distances, modifying is not recommended.
STEP_SIZE = 48
PAIR_OFFSET = 1 * STEP_SIZE  # Distance between paired transistors
PAIR_SHIFT = 1 * STEP_SIZE
ROW_OFFSET = 4 * STEP_SIZE
COL_OFFSET = 6 * STEP_SIZE
START_X = 2 * STEP_SIZE
START_Y = 2 * STEP_SIZE
EXTEND_SIZE = STEP_SIZE // 3

# Change these files to test other circuits
netlist_file = "files/netlist_fivetransistor_ota.txt"
placement_file = "files/placement_fivetransistor_ota.txt"


if __name__ == '__main__':
    netlist = Netlist(filename=netlist_file)
    netlist.parse()
    netlist.print_netlist()
    router = Router(placement_file=placement_file, netlist=netlist, out_file="out_file.asc")
    router.parse_placement()
    router.rotate_mos()
    router.place_mos()
    router.set_all_terminal_coordinates()
    router.extend_mos_terminals()
    router.route()
    router.put_io()
    router.write_flags_to_asc()
    router.write_wire_to_asc()
    router.write_netlist_to_asc()
    print("Total wire cost (Squared): ", router.total_wire_cost())