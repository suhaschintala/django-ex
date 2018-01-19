from django.core.management import BaseCommand
from django.utils import timezone
from hello.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	def handle(self, *args, **options):
		players = Player.objects.all()
		for player in players :
			Log.objects.filter(player_id=player.player_id).update(playerkey=player)
		
