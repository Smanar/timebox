#!/bin/bash

#To debug
#echo "LOG : Params > $*" >> //home//pi//timebox//log.txt
#python2 /home/pi/timebox/timebox.py "$@" &>> //home//pi//timebox//log.txt

python2 /home/pi/timebox/timebox.py "$@" > /dev/null 2>&1 &

exit 0

