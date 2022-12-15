#!/bin/sh
systemctl start promtail
cd /usr/src/app
python main.py
