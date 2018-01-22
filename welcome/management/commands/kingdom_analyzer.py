from django.core.management import BaseCommand
from django.utils import timezone
from welcome.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):   
        cookies = {
            't5mu': 'iFDUrdFRaZ0TVVFM',
            'gl5SessionKey': '%7B%22key%22%3A%22947a758f12c507bf5dc8%22%2C%22id%22%3A%221458675%22%7D',
            'gl5PlayerId': '1458675',
            't5SessionKey': '%7B%22key%22%3A%2294268fd01906c3b09684%22%2C%22id%22%3A%22123%22%7D',
            't5socket': '%22client59ca866462394%22',
            'village': '536657907',
            '_ga': 'GA1.2.181278907.1502519824',
            '_gid': 'GA1.2.392821350.1505613009',
            'msid': '5nmuiuhete114nt19vc8s81fi3',
        }

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://test.kingdoms.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'Referer': 'http://test.kingdoms.com/',
            'Connection': 'keep-alive',
        }

        params = (
            ('c', 'ranking'),
            ('a', 'getRankAndCount'),
        )

        session = input('enter session')
        server = input('enter server')
        kingdomId = input('enter kingdm ID')
        world = GameWorld.objects.get(name=server)
        data = '{"controller":"ranking","action":"getRankAndCount","params":{"id":'+kingdomId+',"rankingType":"ranking_Kingdom","rankingSubtype":"victoryPoints"},"session":"'+session+'"}'
        all_kingdoms = [k.kid for k in Kingdom.objects.filter(world=world)]
        r = requests.post('http://'+server+'.kingdoms.com/api/', headers=headers, params=params, cookies=cookies, data=data)
        json_data = json.loads(r.text)
        num_kingdoms = 0
        if 'response' in json_data :
            num_kingdoms = json_data['response']['numberOfItems']
        else :
            import sys
            sys.exit(0)
        kingdoms = []
        start = 0
        end = num_kingdoms
        data = '{"controller":"ranking","action":"getRanking","params":{"start":'+str(start)+',"end":'+str(end)+',"rankingType":"ranking_Kingdom","rankingSubtype":"population"},"session":"'+session+'"}'
        r = requests.post('http://'+server+'.kingdoms.com/api/', headers=headers, params=params, cookies=cookies, data=data)
        json_data = json.loads(r.text)
        rankingData = json_data['response']['results']
        for rank in rankingData :
            if rank['kingdomId'] not in all_kingdoms : 
                kingdoms.append(Kingdom(kid=rank['kingdomId'], name=rank['name'], world=world))
            else :
                Kingdom.objects.filter(kid=rank['kingdomId'], world=world).update(name=rank['name'])
        Kingdom.objects.bulk_create(kingdoms)