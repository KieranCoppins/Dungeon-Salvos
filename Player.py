#Kieran Coppins

import random

class Player():
	def __init__(self, name):
		#Map Variables
		self.tile = None

		#Player Variables
		self.name = name
		self.health = 100

		#Equiptment Variables
		self.items = {"Head" : None, "Chest" : None, "Legs" : None, "Left Hand" : None, "Right Hand" : None}

		#Inventory Variables
		self.inventory = []
		self.selectedItem = None
		self.inventorySize = 10

		#Fog of War
		self.sightRange = 5

		self.alive = True

	def identify(self):
		return "Player"

	def __str__(self):
		return "@"

	@property
	def health(self):
		return self.__health

	@health.setter
	def health(self, health):
		if health < 0:
			self.__health = 0
		elif health > 100:
			self.__health = 100
		else:
			self.__health = health

		if self.__health == 0:
			self.kill()

	def generateHealthBar(self):
		percentage = round(self.health / 10)
		#print("Health Percentage: {0}".format(percentage))
		bar = ""
		for i in range(percentage):
			bar = bar + "/"
		return bar

	def equipt(self, slot, item):
		self.items[slot] = item

	def calculateDamage(self):
		minDamage = self.items["Left Hand"].minDamage + self.items["Right Hand"].minDamage
		maxDamage = self.items["Left Hand"].maxDamage + self.items["Right Hand"].maxDamage
		return minDamage, maxDamage

	def calculateDefence(self):
		defence = self.items["Head"].defence + self.items["Chest"].defence + self.items["Legs"].defence
		return defence
	
	def setTile(self, map, x, y):
		if self.tile != None:
			self.tile.character = None
		self.tile = map.tiles["{0},{1}".format(x, y,)]
		self.tile.character = self

	def calculateHit(self, damage):
		hit = self.checkHit(damage)
		self.health -= hit
		return hit
	
	def getHitDamage(self):
		minDamage, maxDamage = self.calculateDamage()
		return random.randint(minDamage, maxDamage)

	def checkHit(self, damage):
		hit = damage - self.calculateDefence()
		if hit > 0:
			return hit
		else:
			return 0

	def kill(self):
		print("Player Died")
		self.alive = False

	def pickUp(self, item, map):
		callback = self.equiptItem(item)

		if callback == None:
			map.removeItem(self.tile.x, self.tile.y)
			return

		if len(self.inventory) < self.inventorySize:
			self.inventory.append(item)
			map.removeItem(self.tile.x, self.tile.y)
			if self.selectedItem == None:
				self.selectedItem = item
			return "{0} added to inventory".format(item.name)
		else:
			return "{0} couldn't be added to inventory".format(item.name)

	def equiptItem(self, item):
		id = item.identify()

		if id == "Weapon":
			if self.items["Right Hand"].name == "Fist":
				self.items["Right Hand"] = item
				return None
			elif self.items["Left Hand"].name == "Fist":
				self.items["Left Hand"] = item
				return None
			else:
				return "Userin"

		elif id == "Armour":
			if self.items[item.slot].name == "Nothing":
				self.items[item.slot] = item
				return None
			else:
				return "Userin"
			return None

		elif id == "Consumable":
			return "Userin"


