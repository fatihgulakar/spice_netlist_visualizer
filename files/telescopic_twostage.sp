* /Users/faikbaskaya/Desktop/net2asc/telescopic_twostage.asc
M2 N006 Vinp N008 0 nfet1 l=1u w=4u
M3 N007 Vinn N008 0 nfet1 l=1u w=4u
M4 N003 N005 N006 0 nfet1 l=300n w=4u
M5 N004 N005 N007 0 nfet1 l=300n w=4u
M8 N002 N003 N004 VDD pfet1 l=300n w=8u
M7 N001 N003 N003 VDD pfet1 l=300n w=8u
M9 VDD N001 N001 VDD pfet1 l=1u w=8u
M10 VDD N001 N002 VDD pfet1 l=1u w=8u
M0 N008 Vbias 0 0 nfet1 l=2u w=16u
M6 VDD N004 Vout VDD pfet1 l=0.5u w=32u
M1 Vout Vbias 0 0 nfet1 l=2u w=128u

.model nfet1 NMOS
.model pfet1 PMOS

*>> pairs M2 M3
*>> pairs M4 M5
*>> pairs M7 M8
*>> pairs M9 M10

*>> port input Vinp
*>> port input Vinn
*>> port input Vbias
*>> port output Vout

.backanno
.end
