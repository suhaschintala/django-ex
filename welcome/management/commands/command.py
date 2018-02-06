from django.core.management import BaseCommand
from django.utils import timezone
from welcome.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	def add_arguments(self, parser):
        parser.add_argument('server', nargs='+', type=str)

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
				try :
					data_map[rank['playerId']]["population"] = rank['population']
					data_map[rank['playerId']]["tribe"] = rank['tribeId']
					data_map[rank['playerId']]["kingdomId"] = rank['kingdomId']
				except :
					pass
			else :
				data_map[rank['playerId']] = {}
				data_map[rank['playerId']]['player_name'] = rank['playerName']
				data_map[rank['playerId']][pts] = rank['points']
				try :
					data_map[rank['playerId']]["population"] = rank['population']
					data_map[rank['playerId']]["tribe"] = rank['tribeId']
					data_map[rank['playerId']]["kingdomId"] = rank['kingdomId']
				except :
					pass

	def handle(self, *args, **options):
		server = options['server']
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
		world = GameWorld.objects.get(name=server)
		session = world.session
		data = '{"controller":"ranking","action":"getRankAndCount","params":{"id":3522,"rankingType":"ranking_Player","rankingSubtype":"population"},"session":"'+session+'"}'

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
				player = Player.objects.get(pid=player_id, world=world)
				try :
					kingdom = Kingdom.objects.get(kid=int(pdata['kingdomId']), world=world)	
					# self.stdout.write("" + str(player.id) + '  ' + str(player_id))
					log_list.append(
						Log(timestamp=time, off_score=pdata['offPoints'], deff_score=pdata['deffPoints'], hero_score=pdata['heroes'], population=pdata['population'], player_id=player.id, kingdom_id=kingdom.id,world=world)
					)
				except Kingdom.DoesNotExist:
					kingdom = Kingdom(name="Test Name", kid=int(pdata['kingdomId']), world=world)
					log_list.append(
						Log(timestamp=time, off_score=pdata['offPoints'], deff_score=pdata['deffPoints'], hero_score=pdata['heroes'], population=pdata['population'], player_id=player.id, kingdom_id=kingdom.id,world=world)
					)

			except Player.DoesNotExist:
				try :
					player = Player(name=pdata['player_name'], pid=player_id, capital=0, tribe=int(pdata['tribe']),world=world)
					player.save()
					log_list.append(
						Log(timestamp=time, off_score=pdata['offPoints'], deff_score=pdata['deffPoints'], hero_score=pdata['heroes'], population=pdata['population'], player_id=player_id,world=world)
					)
				except KeyError:
					pass
		self.stdout.write("Yea!! " + str(len(log_list)))
		Log.objects.bulk_create(log_list)
		

