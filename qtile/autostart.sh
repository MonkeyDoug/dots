#!/bin/sh

picom -b
xidlehook \
  --not-when-fullscreen \
  --not-when-audio \
  --timer 33 \
  "i3lock-dracula" \
  "" &
