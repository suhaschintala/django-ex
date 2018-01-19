from django.core.management import BaseCommand
from django.utils import timezone
from hello.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand


class Command(BaseCommand):
	def get_dist(self, villaId, mycoord):
		x = villaId%32768 - 16384
		y = villaId/32768 - 16384
		coord = [x,y]
		dist = (coord[0]- mycoord[0])**2 + (coord[1]- mycoord[1])**2
		return dist**0.5 
	def handle(self, *args, **options):
		server = 'com1'
		mycoord = [1,50]
		players = list(Player.objects.using(server).all())
		near_players = []
		my_map = {}
		for player in players :
			dist = self.get_dist(player.capital, mycoord)
			if dist < 20 :
				near_players.append(player)
				my_map[player.id] = {'obj':player}
		names = '["Player:' + str(near_players[0].id) + '"'
		for pl in near_players[1:] :
			names += ',"Player:'+str(pl.id)+'"'
		names += ']'

		import requests
		cookies = {
		    'zarget_user_id': '1498609681682r0.6579067754092227',
		    't5mu': 'JFUVItWMntUY6BVM',
		    'gl5SessionKey': '%7B%22key%22%3A%22483d869d0f8695241a19%22%2C%22id%22%3A%221458675%22%7D',
		    'gl5PlayerId': '1458675',
		    't5SessionKey': '%7B%22key%22%3A%22d6795b52bda57bc494a1%22%2C%22id%22%3A%22574%22%7D',
		    '_ga': 'GA1.2.1603975367.1498609543',
		    '_gid': 'GA1.2.1791999195.1501968231',
		    't5socket': '%22client5987b07a85a41%22',
		    'village': '536461334',
		    'msid': 'q7k2gae4nnn9ftfpn4n98suiv4',
		}

		headers = {
		    'Pragma': 'no-cache',
		    'Origin': 'http://com1x3.kingdoms.com',
		    'Accept-Encoding': 'gzip, deflate',
		    'Accept-Language': 'en-US,en;q=0.8',
		    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
		    'Content-Type': 'application/json;charset=UTF-8',
		    'Accept': 'application/json, text/plain, */*',
		    'Cache-Control': 'no-cache',
		    'Referer': 'http://com1x3.kingdoms.com/',
		    'Connection': 'keep-alive',
		}
		params = (
		    ('c', 'cache'),
		    ('a', 'get'),
		)

		session = 'df268295339edbdf43f1'
		import json
		data = '{"controller":"cache","action":"get","params":{"names":'+names+'},"session":"'+session+'"}'

		r = requests.post('http://'+server+'.kingdoms.com/api/', headers=headers, params=params, cookies=cookies, data=data)
		import json
		import sys
		data = json.loads(r.text)
		genplayers = data['cache']
		maps = []
		for pl in genplayers :
			pid = pl['data']['playerId']
			# my_map[pid]['prestige'] = pl['data']['prestige']
			shitty = '('+pl['data']['villages'][0]['coordinates']['x']+ '|'+pl['data']['villages'][0]['coordinates']['y']+ ')'
			maps.append((pl['data']['prestige'],pl['data']['name'] + ',' + shitty + ',' + str(pl['data']['prestige'])))
		# for pl in near_players :
		# 	print pl.name, ' (', pl.capital%32768 -16384, '|', pl.capital/32768 - 16384,')'
		maps.sort()
		for each in maps:
			print each[1]	