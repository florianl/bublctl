#!/bin/sh

for i in {0000..9999}
do
    wget -q -t 2 192.168.0.100/file/dcim/100bublc/bubl$i.thm
done
