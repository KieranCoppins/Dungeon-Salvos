#Kieran Coppins

import random

class Weapon():
	def __init__(self, minDamage, maxDamage, name):
		self.minDamage = minDamage
		self.maxDamage = maxDamage

		self.name = name

	def identify(self):
		return "Weapon"

	def __str__(self):
		return "?"

class Armour():
	def __init__(self, name, defence, slot):
		self.name = name
		self.defence = defence

		self.slot = slot

	def identify(self):
		return "Armour"

	def __str__(self):
		return "!"

class Consumable():
	def __init__(self, name, stat, modifier):
		self.name = name
		self.stat = stat
		self.modifier = modifier

	def identify(self):
		return "Consumable"

	def __str__(self):
		return "*"

	def consume(self, player):
		if self.stat == "Health":
			player.health = player.health + self.modifier