#! /usr/bin/python
import speedtest

#takes about 1 minute (a little less)

servers = []
# If you want to test against a specific server
# servers = [1234]

s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
s.download()
s.upload()
s.results.share()

results_dict = s.results.dict()

downMbps = results_dict['download'] / 1000000
upMbps = results_dict['upload'] / 1000000

print('{0:.2f}'.format(downMbps))
print('{0:.2f}'.format(upMbps))