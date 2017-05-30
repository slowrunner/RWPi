#!/bin/bash

#sudo cp /etc/asound.conf /etc/asound.conf.bak
#sudo cp /usr/share/alsa/alsa.conf /usr/share/alsa/alsa.conf.bak
sudo cp -f ./asound.conf /etc/asound.conf
sudo cp -f ./alsa.conf   /usr/share/alsa/alsa.conf
sudo cp ./.bashrc /home/pi
sudo alsactl init
sudo alsactl kill rescan
#sudo alsa force-reload
