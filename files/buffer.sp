* /Users/faikbaskaya/Desktop/net2asc/out_buffer.asc
M2 VDD N001 N002 VDD PMOS l=180n w=2.5u
M3 VDD N002 N003 VDD PMOS l=180n w=2.5u
M5 VDD N003 N004 VDD PMOS l=180n w=2.5u
M7 VDD N004 N005 VDD PMOS l=180n w=2.5u
M1 N002 N001 0 0 NMOS l=180n w=1u
M4 N003 N002 0 0 NMOS l=180n w=1u
M6 N004 N003 0 0 NMOS l=180n w=1u
M8 N005 N004 0 0 NMOS l=180n w=1u
.model NMOS NMOS
.model PMOS PMOS
.backanno
.end
