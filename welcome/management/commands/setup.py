from django.core.management import BaseCommand
from django.utils import timezone
from welcome.models import *
from datetime import datetime
import requests
import json
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):   
        server = input("Name of server :")
        session = input("Session : ")
        world = GameWorld(name=server, session=session)
        world.save()
        def_kingdom = Kingdom(kid=0,world=world, name="NONE")
        def_kingdom.save()