from django.core.management import BaseCommand
from django.utils import timezone
from welcome.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	def handle(self, *args, **options):
		import requests
		import sys
		import datetime
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
		    ('c', 'map'),
		    ('a', 'getByRegionIds'),
		)

		server = 'com1'
		session = '84a801f2c7bb363a8095'
		world = GameWorld.objects.get(name=server)
		import json
		names ='['
		for i in range(-15, 14):
		    for j in range(-15, 14):
		        id = (i+16384) + 32768*(j+16384)
		        if i==-15 and j==-15:
		            names+=str(id)
		        else :
		            names+=',' + str(id)
		names += ']'
		# data = '{"controller":"cache","action":"get","params":{"names":'+names+'},"session":"87d75a4c150f24be5a26"}'
		# print names
		# sys.exit(0)
		data = '{"controller":"map","action":"getByRegionIds","params":{"regionIdCollection":{"1":'+names+',"2":[],"3":[],"4":[],"5":[],"6":[]}},"session":"'+session+'"}'

		r = requests.post('http://'+server+'.kingdoms.com/api/', headers=headers, params=params, cookies=cookies, data=data)
		import json
		import sys
		data = json.loads(r.text)
		regions = data['response']['1']['region']
		players = []
		for key in regions :
			cellid = int(key)
			(y,x) = cellid/32768 - 16384, cellid%32768 - 16384
			# print key , '(',x,',',y,')'
			region = regions[key]
			for cell in region:
				cellid = int(cell['id'])
				(y,x) = cellid/32768 - 16384, cellid%32768 - 16384
				try :
					# self.stdout.write(str(cell['village']))
					if cell['village']['type'] == '1':
						self.stdout.write(str(cell))
						player = Player.objects.filter(pid=int(cell['playerId']), world=world)
						if len(player) == 1 :
							player[0].capital = cellid
							player[0].save()
				except :
					pass
