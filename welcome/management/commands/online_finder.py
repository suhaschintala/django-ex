from django.core.management import BaseCommand
from django.utils import timezone
from hello.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('pid', type=int)
		parser.add_argument('numdays', type=int)

	def robber_print(self, entries):
		maxdiff = 0
		for i in range(0,len(entries) - 1):
			curroffdiff = entries[i+1].off_score - entries[i].off_score
			currherodiff = entries[i+1].hero_score - entries[i].hero_score
			if ( curroffdiff > maxdiff) and (currherodiff > curroffdiff*1.5):
				maxdiff = curroffdiff
		return maxdiff

	def handle(self, *args, **options):
		pid = options['pid']
		print pid
		server = 'com2x3'
		from datetime import datetime, timedelta
		numdays = options['numdays']
		recdate = datetime.now() - timedelta(days=numdays)
		recent_logs = list(Log.objects.using(server).filter(player__id=pid).filter(timestamp__gt=recdate).select_related('player'))
		datebucket = [[] for x in range(0,24)]
		for i  in range(1, len(recent_logs)): 
			log = recent_logs[i]
			datebucket[log.timestamp.hour].append(log.population - recent_logs[i-1].population)
		for i in range(0,24):
			print i, sum(datebucket[i])	
		# player_map = {}
		# for each in recent_logs :
		# 	try :
		# 		player_map[each.player.name].append(each)
		# 	except :
		# 		player_map[each.player.name]=[each]
		# for key in player_map :
		# 	player_map[key] = self.sleep_print(player_map[key])

		# for key, value in sorted(player_map.iteritems(), key=lambda (k,v): (v,k)):
		# 	print "%s : %s" % (key, value)
