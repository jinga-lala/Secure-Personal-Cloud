#!/bin/sh
eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)";
path="$1""/Secure_Personal_Cloud/linux/main.py"
#Code:
var=$(python3 $path auto_check 2>&1 1>/dev/null)
# DISPLAY=:0 notify-send 2
# echo "ehr""$var""there"
DISPLAY=:0 notify-send "Secure-Personal-Cloud" "$var"
