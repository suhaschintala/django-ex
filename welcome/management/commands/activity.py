from django.core.management import BaseCommand
from django.utils import timezone
from hello.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):

	def distance(self, coord1, coord2):
		return ((coord1[1]-coord2[1])**2 + (coord1[0]-coord2[0])**2)**(0.5)

	def analyze(self, entries, mycoords, maxdistance):
		maxdiff = 0
		maxhpdiff  = 0
		for i in range(0,len(entries) - 1):
			curroffdiff = entries[i+1].off_score - entries[i].off_score
			currherodiff = entries[i+1].hero_score - entries[i].hero_score
			currpopdiff = entries[i+1].population - entries[i].population
			if ( curroffdiff > maxdiff) and (currherodiff > curroffdiff*1.5):
				maxdiff = curroffdiff
				maxhpdiff = currherodiff
		capital = entries[-1].player.capital
		kingdom = 'NONE'
		try :
			kingdom = entries[-1].kingdom.name
		except :
			pass
		coords = (capital%32768 - 16384, capital/32768 - 16384)
		if distance(coords, mycoords) <= maxdistance :
			return (maxdiff, maxhpdiff, coords, kingdom)
		else :
			return None
		
	def handle(self, *args, **options):
		server = 'com1x3'
		mycoords = (-16,2)
		maxdistance = 10
		from datetime import datetime, timedelta
		recdate = datetime.now() - timedelta(hours=6)
		recent_logs = list(Log.objects.using(server).filter(timestamp__gt=recdate).select_related('player', 'kingdom'))
		player_map = {}
		for each in recent_logs :
			try :
				player_map[each.player.name].append(each)
			except :
				player_map[each.player.name]=[each]
		for key in player_map :
			player_map[key] = self.analyze(player_map[key], mycoords, maxdistance)

		for key, value in sorted(player_map.iteritems(), key=lambda (k,v): (v,k)):
			print "%s : %s -- %s -- (%d,%d) -- %s" % (key, value[0], value[1], value[2][0], value[2][1], value[3])
