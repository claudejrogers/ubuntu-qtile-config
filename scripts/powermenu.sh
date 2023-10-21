#!/bin/sh

option1=" 󰍃 logoff"
option2="  reboot"
option3=" 󰐥 shutdown"

options="$option1\n$option2\n$option3"

choice=$(echo "$options" | rofi -dmenu -i -no-show-icons -l 3 -width 30 -p "Powermenu")

case $choice in
    $option1)
        qtile cmd-obj -o cmd -f shutdown ;;
    $option2)
        systemctl reboot ;;
    $option3)
        systemctl poweroff ;;
esac