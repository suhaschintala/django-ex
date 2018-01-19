from django.db import models

# Create your models here.

class PageView(models.Model):
    hostname = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

class GameWorld(models.Model):
	name = models.CharField(max_length=10, default="com1x3")
	session = models.CharField(max_length=50, default="None")

class Player(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=20)
	capital = models.IntegerField()
	tribe = models.IntegerField()

class Kingdom(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50, default="None")


class Log(models.Model):
	timestamp = models.DateTimeField('date created')
	off_score = models.IntegerField()
	deff_score = models.IntegerField()
	hero_score = models.IntegerField()
	population = models.IntegerField(default=0)
	player = models.ForeignKey(Player, default=None)
	kingdom = models.ForeignKey(Kingdom, default=None, null=True)
