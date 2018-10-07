#! /usr/bin/python
import time
import subprocess
import signal
import os
from pathlib import Path

#sudo airmon-ng start wlan1
cmd = 'sudo airodump-ng --bssid "CC:33:BB:BA:6F:A5" --channel 48 -w capture wlan1mon --write-interval 1 --output-format pcap'

file = Path() / 'capture-01.cap'
previousSize = 0
while True:
	airodump = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	for s in range(0, 59):
		if(file.exists()):
			size = file.stat().st_size
			print(size - previousSize)
			previousSize = size
			time.sleep(1)

	#airodump.kill()
	#os.killpg(os.getpgid(airodump.pid), signal.SIGTERM)
#	if(file.exists()):
#		print(str(file.resolve()))
#		os.remove(str(file.resolve()))