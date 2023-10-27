To test the program follow these instructions:

1.  At the lines 16 & 17 of Router.py file, there are two variables called <netlist_file> and <placement_file>.
Enter the SPICE netlist name to netlist_file and placement file name to other. These two files must be at same folder with
Router.py

2.  After changing the files name, simply run Router.py file. If you have Python installed, running

	python Router.py

from command line should work. Then, the file out_file.asc will be generated. This has all transistors in the netlist
and wires connecting them.

3.  Simply open out_file.asc in LTspice.


SPICE Netlist File   			        Placement File
------------------			          ---------------
buffer.sp				                  buffer.txt
telescopic_twostage.sp			      telescopic_twostage.txt
netlist_fivetransistor_ota.txt		placement_fivetransistor_ota.txt
netlist_nand2.txt			            placement_nand2.txt


buffer.asc and telescopic_twostage.asc files are the original schematics.