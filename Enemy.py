#Kieran Coppins

class Enemy():
	def __init__(self, name, health, damage, graphic):
		self.name = name
		self.health = health
		self.damage = damage

		self.graphic = graphic

		self.tile = None

		self.lineOfSight = 3

		self.alive = True

		#Path finding Variables
		self.currentPath = []
		self.moveSpeed = 1
		self.target = None

	def identify(self):
		return "Enemy"

	def __str__(self):
		return self.graphic

	def die(self):
		if self.tile != None:
			self.tile.character = None
			self.alive = False
		

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
			self.die()

	def setTile(self, map, x, y):
		if self.tile != None:
			self.tile.character = None
		self.tile = map.tiles["{0},{1}".format(x, y,)]
		self.tile.character = self

	def checkPlayer(self, player, map):
		startX = self.tile.x - self.lineOfSight
		startY = self.tile.y - self.lineOfSight

		endX = self.tile.x + self.lineOfSight
		endY = self.tile.y + self.lineOfSight

		iX = startX
		iY = startY

		for iX in range(startX, endX):
			for iY in range(startY, endY):
				if iX < 0:
					iX = 0
				if iY < 0:
					iY = 0
				if iX >= map.width - 1:
					iX = map.width - 1
				if iY >= map.height - 1:
					iY = map.height - 1
				if map.tiles["{0},{1}".format(iX, iY)].character == player:
					self.target = player.tile
					map.generatePathTo(self)

	def moveToNextTile(self, graph, player):
		remainingMovement = self.moveSpeed

		while remainingMovement > 0:
			if len(self.currentPath) == 0:
				return

			remainingMovement -= 1
			if self.currentPath[1].x == player.tile.x and self.currentPath[1].y == player.tile.y:
				return "combat"
			self.setTile(graph, self.currentPath[1].x, self.currentPath[1].y)
			self.currentPath.remove(self.currentPath[0])

			if len(self.currentPath) == 1:
				self.currentPath.remove(self.currentPath[0])

			return None

