import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView
from django.http import JsonResponse
import json
from .models import Log, Player, Kingdom, GameWorld
from datetime import datetime, timedelta
from django.utils import timezone
from django.core import serializers
# Create your views here.

def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    return HttpResponse(PageView.objects.count())


def playerpage(request):
	return render(request, 'player.html')

def timepage(request):
	return render(request, 'timeanalysis.html')

def onlinepage(request):
	return render(request, 'online_finder.html')

def attackpage(request):
	return render(request, 'attack_analyzer.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def playerdata(request):
	playerName = request.GET.get('name','None')
	worldName= request.GET.get('server', 'com1x3')
	playerId = '129'
	if playerName is not 'None':
		playerId = str(Player.objects.filter(name=playerName)[0].pid)
	else :
		playerId = request.GET.get('playerId','129')
	world = None
	try :
		world = GameWorld.objects.get(name=worldName)
	except :
		raise Http404("Game world does not exist")

	playerId = int(playerId)
	print(playerId)
	print(worldName)

	def_kingdom  = Kingdom.objects.get(kid=0,world=world)
	kname = ''
	plogs = list(Log.objects.filter(player__pid=playerId, world=world).select_related('player', 'kingdom'))
	final_logs = []
	
	for log in plogs :
		if not log.kingdom :
			kname = def_kingdom.name
		else :
			kname = log.kingdom.name
		dict = {
			'player_name' : log.player.name,
			'off_score'		: log.off_score,
			'deff_score'	: log.deff_score,
			'hero_score'	: log.hero_score,
			'capital'		: log.player.capital,
			'timestamp'		: log.timestamp,
			'tribe'			: log.player.tribe,
			'pop'			: log.population,
			'kingdom'		: kname
		}
		final_logs.append(dict)
	# plogs = serializers.serialize('json', plogs)
	json_dict = {'logs' : final_logs}
	return JsonResponse(json_dict)

def kingdomeanalysis(request):
	worldName= request.GET.get('server', 'com1x3')
	kingdomName= request.GET.get('name', 'NONE')
	days= int(request.GET.get('days', '7'))
	# logs = Log.objects.filter(timestamp__gt=)


def timeintervaldata(request):
	import pytz
	date = request.GET.get('date','2017-08-09')
	time = request.GET.get('time', '22:08')
	interval = request.GET.get('interval', '30')
	worldName= request.GET.get('server', 'com1x3')
	world = None
	try :
		world = GameWorld.objects.get(name=worldName)
	except :
		raise Http404("Game world does not exist")
	interval = int(interval)
	year, month, day = [int(x) for x in date.split('-')]
	hour, minute = [int(x) for x in time.split(':')]
	prev_date = datetime(year,month,day,hour,minute) - timedelta(minutes=interval)
	next_date = datetime(year,month,day,hour,minute) + timedelta(minutes=interval)
	def_kingdom  = Kingdom.objects.get(kid=0,world=world)
	kname = ''
	logs = list(Log.objects.filter(timestamp__range=(prev_date, next_date), world=world).select_related('player', 'kingdom'))
	final_logs = []
	for log in logs :
		if not log.kingdom :
			kname = def_kingdom.name
		else :
			kname = log.kingdom.name
		dict = {
			'player_name' : log.player.name,
			'off_score'		: log.off_score,
			'deff_score'	: log.deff_score,
			'hero_score'	: log.hero_score,
			'capital'		: log.player.capital,
			'timestamp'		: log.timestamp,
			'player_id'		: log.player.pid,
			'tribe'			: log.player.tribe,
			'kingdom'		: kname
		}
		final_logs.append(dict)
	json_dict = {'logs' : final_logs}
	return JsonResponse(json_dict)


def onlinedata(request):
	playerName = request.GET.get('name','None')
	worldName= request.GET.get('server', 'com1x3')
	world = GameWorld.objects.get(world=worldName)
	days= request.GET.get('days', '5')
	playerId = '129'
	if playerName is not 'None':
		playerId = str(Player.objects.filter(name=playerName,world=world)[0].pid)
	else :
		playerId = request.GET.get('playerId','129')
	playerId = int(playerId)

	world = None
	try :
		world = GameWorld.objects.get(name=worldName)
	except :
		raise Http404("Game world does not exist")

	days = int(days)
	from datetime import datetime, timedelta
	recdate = datetime.now() - timedelta(days=days)
	recent_logs = list(Log.objects.filter(player__pid=playerId, world=world).filter(timestamp__gt=recdate).select_related('player'))
	datebucket = [[] for x in range(0,24)]
	for i  in range(1, len(recent_logs)): 
		log = recent_logs[i]
		datebucket[log.timestamp.hour].append(log.population - recent_logs[i-1].population)
	final_data = []
	for each in datebucket  :
		final_data.append(sum(each))
	json_dict = {'data':datebucket}
	return JsonResponse(json_dict)

def attack_analyzer(request):
	import requests
	session = request.GET.get('session','None')
	server= request.GET.get('server', 'com1x3')
	params = (
		('c', 'village'),
		('a', 'getKingdomVillageAttacks'),
	)
	data = '{"controller":"village","action":"getKingdomVillageAttacks","params":{},"session":"'+session+'"}'
	
	def gettime(timestamp):
		return ((datetime.fromtimestamp(int(timestamp)) + timedelta(hours=1)))

	def time_sent(time_arrived, id1,id2,speed):
		coord1 = getcoordstuple(id1)
		coord2 = getcoordstuple(id2)
		speed = input()
		dist = ((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)**(0.5)
		time = ((dist*1.0000) / (speed*1.000))
		return (datetime.datetime.fromtimestamp(int(time_arrived)) - datetime.timedelta(hours=4,minutes=30) - datetime.timedelta(hours=time)).strftime('%Y-%m-%d %H:%M:%S')

	def getcoordstuple(id):
		cid = int(id)
		x = cid%32768 - 16384
		y = cid/32768 - 16384
		return (x,y)

	def getcoords(id):
		cid = int(id)
		x = cid%32768 - 16384
		y = cid/32768 - 16384
		return '('+str(x)+','+str(y)+')'
	

	cookies = {
		'_ga': 'GA1.2.906435046.1502520632',
		'_gid': 'GA1.2.2066748333.1507983185',
		't5mu': '6JVQ0cHeopWW6NHR',
		'msid': '5ukoskrbf1m4eh96buv6fbr7h2',
		'gl5SessionKey': '%7B%22key%22%3A%22a73bd9189f1a4bebe22b%22%2C%22id%22%3A%221458675%22%7D',
		'gl5PlayerId': '1458675',
		't5SessionKey': '%7B%22key%22%3A%22ef0b9b7b221ea92815b2%22%2C%22id%22%3A%22590%22%7D',
		't5socket': '%22client5a0219e811e30%22',
		'village': '536985632',
	}

	headers = {
		'Host': 'com2x3.kingdoms.com',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Content-Type': 'application/json;charset=utf-8',
		'Referer': 'https://com2x3.kingdoms.com/',
		'Connection': 'keep-alive',
	}

	r = requests.post('http://'+server+'.kingdoms.com/api/', params=params, headers=headers, cookies=cookies, data=data)
	import json
	data = json.loads(r.text)
	final_data = []
	if 'cache' in data :
		for village in data['cache']:
			for attack in village['data']['cache']:
				att_data = attack['data']
				our_dict = {}
				scoords = getcoordstuple(att_data['villageIdStart'])
				dcoords = getcoordstuple(att_data['villageIdTarget'])
				our_dict['sourceX'] = scoords[0]
				our_dict['sourceY'] = scoords[1]
				our_dict['targetX'] = dcoords[0]
				our_dict['targetY'] = dcoords[1]
				our_dict['distance'] = ((scoords[0] - dcoords[0])**2 + (scoords[1] - dcoords[1])**2)**(0.5)
				our_dict['time_reached']=gettime(att_data['timeFinish'])
				if att_data['movementType'] == '4':
					our_dict['type'] = 'Raid'
					# string+= '\n'+ getcoords(att_data['villageIdStart']) + ' raids ' + getcoords(att_data['villageIdTarget']) + ' at ' + gettime(att_data['timeFinish'])+' :: Sent at '+ time_sent(att_data['timeFinish'], att_data['villageIdStart'], att_data['villageIdTarget'], 1)
				if att_data['movementType'] == '3':
					our_dict['type'] = 'Attack'
					# string+= '\n'+  getcoords(att_data['villageIdStart']) + ' attacks ' + getcoords(att_data['villageIdTarget']) + ' at ' + gettime(att_data['timeFinish'])+' :: Sent at '+ time_sent(att_data['timeFinish'], att_data['villageIdStart'], att_data['villageIdTarget'], 1)
				if att_data['movementType'] == '47':
					our_dict['type'] = 'Seige'
					# string+= '\n'+  getcoords(att_data['villageIdStart']) + ' SIEGES ' + getcoords(att_data['villageIdTarget']) + ' at ' + gettime(att_data['timeFinish'])+' :: Sent at '+ time_sent(att_data['timeFinish'], att_data['villageIdStart'], att_data['villageIdTarget'], 1)
				final_data.append(our_dict)
	json_dict = {'data': final_data}
	return JsonResponse(json_dict)

def activity(request):
	days = int(request.GET.get('days', '0'))
	hours = int(request.GET.get('hours','5'))
	server = request.GET.get('server', 'com5')
	x = int(request.GET.get('x', '0'))
	y = int(request.GET.get('y', '0'))
	dist = int(request.GET.get('distance','10'))

	ldate = datetime.now() - timedelta(days=days,hours=hours)
	players = {p.id:p for p in list(Player.objects.all())}
	kingdoms = list(Kingdom.objects.all())
	logs = list(Log.objects.filter(timestamp__gt=ldate))
	player_map = {}
	for log in logs :
		player = players[log.player]

		try :
			player_map[log.player].append(log)
		except :
			player_map[log.player] = [log]
	results = []
	for pid in player_map :
		plogs= player_map[pid]
		
	return JsonResponse({})


def update_world(request):
	session = request.GET.get('session','None')
	name= request.GET.get('name', 'com1x3')
	world = GameWorld.objects.get(name=name)
	world.session = session
	world.save()
	return HttpResponse("<h1>Server details saved</h1>")

def update_log(request):
	server= request.GET.get('server', 'com2x3')
	world = GameWorld.objects.get(name=server)
	from welcome.management.commands.command import Command
	x = Command()
	x.handle(server=server)
	return HttpResponse("The stats are logged! :)")

