#!/bin/sh

picom &
dunst &
lxsession &
lxpolkit &
xidlehook --not-when-fullscreen --not-when-audio --timer 60 "i3lock-fancy-dualmonitor" "" &
