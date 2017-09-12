#!/bin/bash

snmpwalk -v 2c -c public@10 -OXsq 10.0.0.3 .1.3.6.1.2.1.17.4.3.1.1 > /home/catalin/Workspace/mac-logging/input.txt;
