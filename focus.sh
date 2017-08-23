#!/bin/sh

cmd(){
    ps aux | grep -c $1
}

count=cmd $1
echo $count
if [! cmd $1 -eq 0 ]; then
    $1
else
    i3-msg "[class="+$1+"] focus"
fi
