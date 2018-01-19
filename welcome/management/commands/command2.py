from django.core.management import BaseCommand
from django.utils import timezone
from hello.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):

	def addRankingData(self, data_map, start, end, pts, server , session, headers, cookies):
		params = (
		    ('c', 'ranking'),
		    ('a', 'getRanking'),
		    ('t1502065843517', ''),
		)
		data = '{"controller":"ranking","action":"getRanking","params":{"start":'+str(start)+',"end":'+str(end)+',"rankingType":"ranking_Player","rankingSubtype":"'+pts+'"},"session":"'+session+'"}'
		r = requests.post('http://'+server+'.kingdoms.com/api/', headers=headers, params=params, cookies=cookies, data=data)
		json_data = json.loads(r.text)
		rankingData = json_data['response']['results']
		for rank in rankingData :
			if rank['playerId'] in data_map :
				data_map[rank['playerId']]['player_name'] = rank['playerName']
				data_map[rank['playerId']][pts] = rank['points']
			else :
				data_map[rank['playerId']] = {}
				data_map[rank['playerId']]['player_name'] = rank['playerName']
				data_map[rank['playerId']][pts] = rank['points']


	def handle(self, *args, **options):
		
		cookies = {
			'gl5SessionKey': '%7B%22key%22%3A%221e145327d5c1080f45ff%22%2C%22id%22%3A%221458675%22%7D',
			'gl5PlayerId': '1458675',
			't5SessionKey': '%7B%22key%22%3A%221c70feea7bba022fc5e0%22%2C%22id%22%3A%22744%22%7D',
			't5mu': 'wV1YxoUa3hWZuV0b',
			'_ga': 'GA1.2.181278907.1502519824',
			'_gid': 'GA1.2.956245803.1502828072',
			't5socket': '%22client5995aee4306e6%22',
			'village': '537313306',
			'msid': '5nmuiuhete114nt19vc8s81fi3',
		}

		headers = {
			'Pragma': 'no-cache',
			'Origin': 'http://com2.kingdoms.com',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en-US,en;q=0.8',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
			'Content-Type': 'application/json;charset=UTF-8',
			'Accept': 'application/json, text/plain, */*',
			'Cache-Control': 'no-cache',
			'Referer': 'http://com2.kingdoms.com/',
			'Connection': 'keep-alive',
		}


		params = (
		    ('c', 'ranking'),
		    ('a', 'getRankAndCount'),
		    ('t1502065740553', ''),
		)
		session = "1bb0cc06627cc7150d0b"
		server = "com2"
		data = '{"controller":"ranking","action":"getRankAndCount","params":{"id":744,"rankingType":"ranking_Player","rankingSubtype":"population"},"session":"'+session+'"}'

		r = requests.post('http://'+server+'.kingdoms.com/api/', headers=headers, params=params, cookies=cookies, data=data)
		self.stdout.write('olol')
		json_data = json.loads(r.text)
		numPlayers = 0
		if 'response' in json_data :
			numPlayers = json_data['response']['numberOfItems']
		else :
			import sys
			sys.exit(0)


		data_map = {}
		pts_formats = ['offPoints', 'deffPoints', 'heroes']
		start = 0
		while start < numPlayers :
			end = start + 999
			if end > numPlayers :
				end = numPlayers - 1
			for pts in pts_formats :
				self.addRankingData(data_map, start, end, pts, server , session, headers, cookies)
			start = start + 1000

		time = timezone.now()
		log_list = []
		for player_id in data_map :
			pdata = data_map[player_id]
			player= None
			try :
				player = Player.objects.using(server).get(player_id=player_id)
				log_list.append(
					Log(timestamp=time, player_name=pdata['player_name'], off_score=pdata['offPoints'], deff_score=pdata['deffPoints'], hero_score=pdata['heroes'], player_id=int(player_id), playerkey=player)
				)
			except Player.DoesNotExist:
				try :
					player = Player(player_name=pdata['player_name'], player_id=player_id, capital=0)
					player.save(using=server)
					log_list.append(
						Log(timestamp=time, player_name=pdata['player_name'], off_score=pdata['offPoints'], deff_score=pdata['deffPoints'], hero_score=pdata['heroes'], player_id=int(player_id), playerkey=player)
					)
				except KeyError:
					pass
		Log.objects.using(server).bulk_create(log_list)