#!/bin/bash
# default sample rate is 5 microseconds or 10% of PiB+
# running pigpiod with 10 microseconds sample rate drops load to 6%
#
sudo pigpiod -s 10