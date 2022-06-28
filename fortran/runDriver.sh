#!/bin/bash

if [ -f SimulDetect.dat ]; then
    \rm SimulDetect.dat
fi
if [ -f SimulTrack.dat ]; then
    \rm SimulTrack.dat
fi

#make sure you have ~1 Gb of free memory before you download these!
vcp vos:NewHorizons/2021ModelKuiperBelt/NKB3_0.txt .
#can download more models by changing _0 to _1 - _20

#this runs the survey simulator on whatever is in ReadModelFromFile.in - check that file before you start!
./Driver < ReadModelFromFile.in

#python plotRAdec.py
