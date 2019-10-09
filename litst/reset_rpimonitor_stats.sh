#!/bin/bash

sudo service rpimonitor stop
sudo rm -r /var/lib/rpimonitor/stat
sudo service rpimonitor start
echo "RPI-Monitor Stats Reset Complete"

