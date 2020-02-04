#Kieran Coppins

import math
import random

class Room():
	def __init__(self, x, y, width, height, doors):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.centreX = x + (width // 2)
		self.centreY = y + (height // 2)

		self.tileCoords = []

		self.doors = doors

		self.connected = False

		self.doorCoords = []

	def create(self, map):
		startX = self.x
		startY = self.y

		endX = self.x + self.width
		endY = self.y + self.height

		if startX >= map.width:
			return False
		if startY >= map.height:
			return False


		if endX >= map.width:
			endX = map.width - 1
			self.width = endX - startX
		if endY >= map.height:
			endY = map.height - 1
			self.width = endY - startY

		if self.width < 0:
			self.width = self.width * -1

		if self.height < 0:
			self.height = self.height * -1

		if self.width < map.minRoomSize or self.height < map.minRoomSize:
			return False

		self.centreX = self.x + (self.width // 2)
		self.centreY = self.y + (self.height // 2)


		for x in range(startX, endX):
			for y in range(startY, endY):
				keyword = "{0},{1}".format(x, y)
				self.tileCoords.append(keyword)

		return True

	def intersects(self, otherRoom):
		for roomCoord in self.tileCoords:
			for otherCoord in otherRoom.tileCoords:
				if roomCoord == otherCoord:
					return True

	def createDoorNode(self, map):
		for i in range(self.doors):
			side = random.randint(1, 4)
			if side == 1:
				doorX = self.x
				doorY = random.randint(self.y, self.y + self.height)

			if side == 2:
				doorX = self.x + self.width
				doorY = random.randint(self.y, self.y + self.height)

			if side == 3:
				doorX = random.randint(self.x, self.x + self.width)
				doorY = self.y + self.height

			if side == 4:
				doorX = random.randint(self.x, self.x + self.width)
				doorY = self.y

			keyword = "{0},{1}".format(doorX, doorY)
			self.doorCoords.append(keyword)
			map.doorCoords.append(keyword)


class Map():
	def __init__(self, width, height, maxRoomSize, minRoomSize, minRooms, maxRooms):
		self.height = height
		self.width = width

		self.tiles = {}

		self.rooms = []

		self.doorCoords = []

		self.maxRoomSize = maxRoomSize
		self.minRoomSize = minRoomSize

		self.minRooms = minRooms
		self.maxRooms = maxRooms

	def getEmptyTile(self):
		while True:
			randomX = random.randint(1, self.width - 5)
			randomY = random.randint(1, self.height - 5)

			if self.tiles["{0},{1}".format(randomX, randomY)].type == 0:
				return self.tiles["{0},{1}".format(randomX, randomY)]

	def generateStaircase(self):
		randomRoomInt = random.randint(0, len(self.rooms) - 1)
		room = self.rooms[randomRoomInt]
		randomTileInt = random.randint(0, len(room.tileCoords) - 1)
		tile = room.tileCoords[randomTileInt]
		#print(tile)
		self.tiles[tile].type = 2

	def generateDungeon(self):
		print("populating map")
		self.populateMap(1)
		print("Generating Rooms")
		self.placeRooms(random.randint(self.minRooms, self.maxRooms))
		print("Creating Corridors")
		self.optimisedJoinDoors()
		print("Creating Staircase")
		self.generateStaircase()

	def placeRooms(self, roomCount):
		self.rooms = []
		for r in range(roomCount):
			roomX = random.randint(1, self.width - 1)
			roomY = random.randint(1, self.height - 1)

			roomWidth = random.randint(self.minRoomSize, self.maxRoomSize)
			roomHeight = random.randint(self.minRoomSize, self.maxRoomSize)

			newRoom = Room(roomX, roomY, roomWidth, roomHeight, 1)
			success = newRoom.create(self)
			if success == True:
				newRoom.createDoorNode(self)

				failed = False

				for otherRooms in self.rooms:
					if newRoom.intersects(otherRooms):
						failed = True
						break

				if failed == False:
					self.createRoom(newRoom)
					self.rooms.append(newRoom)

	def joinDoors(self):
		print(self.doorCoords)
		for door in self.doorCoords:
			for otherDoor in self.doorCoords:
				if door != otherDoor:
					path = self.optimisedGenerateCorridors(door, otherDoor)
					self.optimisedCreateCorridor(path)

	def optimisedJoinDoors(self):
		for room in self.rooms:
			if room.connected == False:
				for otherRoom in self.rooms:
					if otherRoom.connected == False:
						roomCoord = "{0},{1}".format(room.centreX, room.centreY)
						otherRoomCoord = "{0},{1}".format(otherRoom.centreX, otherRoom.centreY)
						path = self.optimisedGenerateCorridors(roomCoord, otherRoomCoord)
						self.optimisedCreateCorridor(path)
						room.connected = True
						otherRoom.connected = True

	def optimisedCreateCorridor(self, path):
		for coord in path:
			coordX, coordY = coord.split(",")
			coordX = int(coordX)
			coordY = int(coordY)
			if coordX > 0 and coordX < self.width and coordY > 0 and coordY < self.height:
				self.tiles[coord].type = 0

	def optimisedGenerateCorridors(self, doorA, doorB):
		#print("New Corridor")
		doorAX, doorAY = doorA.split(",")
		doorBX, doorBY = doorB.split(",")

		doorAX = int(doorAX)
		doorAY = int(doorAY)
		doorBX = int(doorBX)
		doorBY = int(doorBY)

		#print("A", doorA)
		#print("B", doorB)

		currentPath = []
		
		if doorBX <= doorAX and doorBY >= doorAY:
			for x in range(doorBX, doorAX + 1):
				currentPath.append("{0},{1}".format(x, doorAY))

			for y in range(doorAY, doorBY + 1):
				currentPath.append("{0},{1}".format(doorBX, y))

		if doorBX >= doorAX and doorBY >= doorAY:
			for x in range(doorAX, doorBX + 1):
				currentPath.append("{0},{1}".format(x, doorBY))

			for y in range(doorAY, doorBY + 1):
				currentPath.append("{0},{1}".format(doorAX, y))

		if doorBX >= doorAX and doorBY <= doorAY:
			for x in range(doorAX, doorBX + 1):
				currentPath.append("{0},{1}".format(x, doorAY))

			for y in range(doorBY, doorAY + 1):
				currentPath.append("{0},{1}".format(doorBX, y))

		if doorBX <= doorAX and doorBY <= doorAY:
			for x in range(doorBX, doorAX + 1):
				currentPath.append("{0},{1}".format(x, doorBY))

			for y in range(doorBY, doorAY + 1):
				currentPath.append("{0},{1}".format(doorAX, y))

		#print("Path", currentPath)
		return currentPath

	def generateCorridors(self, doorA, doorB):
		#Use path finding to find paths between door way nodes generated in room generation
		#If the corridor is x to long, create another door node that other corridors can connect to
		#Thus creating a non-linear map design
		graph = self.generatePathingGraph()
		currentPath = []

		dist = {}
		prev = {}

		unvisited = []

		source = graph[doorA]
		target = graph[doorB]

		dist[source] = 0
		prev[source] = None

		for v in graph:
			v = graph[v]
			if v != source:
				dist[v] = math.inf
				prev[v] = None
			unvisited.append(v)

		while len(unvisited) > 0:
			u = None

			for possibleU in unvisited:
				if u == None or dist[possibleU] < dist[u]:
					u = possibleU

			if u == target:
				break
				
			unvisited.remove(u)

			for v in u.neighbours:
				alt = dist[u] + 1
				if alt < dist[v]:
					dist[v] = alt
					prev[v] = u

		if prev[target] == None:
			return

		currentPath = []
		curr = target

		while curr != None:
			currentPath.append(curr)
			curr = prev[curr]

		currentPath.reverse()
		return currentPath

	def createCorridor(self, path):
		#print("New Path")
		#print(path)
		for node in path:
			#print(node)
			self.tiles["{0},{1}".format(node.x, node.y)].type = 0


	def createRoom(self, room):
		for coord in room.tileCoords:
			self.tiles[coord].type = 0

	def generateTestMap(self):
		self.populateMap(0)
		self.createBorder()
		self.generateWalls()

	def populateMap(self, type):
		for x in range(self.width):
			for y in range(self.height):
				keyword = "{0},{1}".format(x, y)
				self.tiles[keyword] = Tile(x, y, 0)
				self.tiles[keyword].type = type
				#self.tiles[keyword] = Tile(x, y, type)

	def createBorder(self):
		for x in range(self.width):
			for y in range(self.height):
				if x == 0 or x == self.width - 1:
					keyword = "{0},{1}".format(x, y)
					self.tiles[keyword].type = 1
				elif y == 0 or y == self.height - 1:
					keyword = "{0},{1}".format(x, y)
					self.tiles[keyword].type = 1

	def generateWalls(self):
		self.generateWall(self.tiles["0,5"], self.tiles["5,5"])
		self.generateWall(self.tiles["5,0"], self.tiles["5,5"])
		self.generateWall(self.tiles["0,7"], self.tiles["5,7"])
		self.generateWall(self.tiles["3,7"], self.tiles["3,10"])
		self.generateWall(self.tiles["0,10"], self.tiles["3,10"])
		self.tiles["3,5"].type = 0
		self.tiles["1,7"].type = 0

	def generateWall(self, tileA, tileB):
		startX = tileA.x
		startY = tileA.y
		
		endX = tileB.x
		endY = tileB.y

		for x in range(startX, endX + 1):
			for y in range(startY, endY + 1):
				self.tiles["{0},{1}".format(x, y)].type = 1

	#Text based display map
	def displayMap(self, UI):
		UI.clearMap()		
		UI.map.config(state="normal")
		for x in range(self.width):
			for y in range(self.height):
				keyword = "{0},{1}".format(x, y)
				if self.tiles[keyword].visible == False:
					UI.printMap(" ")
				elif self.tiles[keyword].character != None:
					if self.tiles[keyword].character.identify() == "Player":
						tag = "player"
					else:
						tag = "enemy"
					UI.printMap(self.tiles[keyword].character, tag)
				elif self.tiles[keyword].entity != None:
					if self.tiles[keyword].entity.identify() == "Armour":
						tag = "armour"
					elif self.tiles[keyword].entity.identify() == "Weapon":
						tag = "weapon"
					else:
						tag = "consumable"
					UI.printMap(self.tiles[keyword].entity, tag)
				else:
					UI.printMap(self.tiles[keyword])
			UI.printMap("\n")

		UI.map.config(state="disabled")

	def placeItem(self, x, y, item):
		self.tiles["{0},{1}".format(x, y)].entity = item

	def removeItem(self, x, y):
		self.tiles["{0},{1}".format(x, y)].entity = None

	def generatePathingGraph(self):
		graph = {}
		for x in range(self.width):
			for y in range(self.height):
				graph["{0},{1}".format(x, y)] = Node(x, y)

		for x in range(self.width):
			for y in range(self.height):
				if x > 0:
					graph["{0},{1}".format(x, y)].neighbours.append(graph["{0},{1}".format(x - 1, y)])
				if x < self.width - 1:
					graph["{0},{1}".format(x, y)].neighbours.append(graph["{0},{1}".format(x + 1, y)])
				if y > 0:
					graph["{0},{1}".format(x, y)].neighbours.append(graph["{0},{1}".format(x, y - 1)])
				if y < self.height - 1:
					graph["{0},{1}".format(x, y)].neighbours.append(graph["{0},{1}".format(x, y + 1)])

		return graph

	def generatePathTo(self, entity):
		graph = self.generatePathingGraph()
		entity.currentPath = []
		if entity.target == None:
			return

		dist = {}
		prev = {}

		unvisited = []

		source = graph["{0},{1}".format(entity.tile.x, entity.tile.y)]
		target = graph["{0},{1}".format(entity.target.x, entity.target.y)]

		dist[source] = 0
		prev[source] = None

		for v in graph:
			v = graph[v]
			if v != source:
				dist[v] = math.inf
				prev[v] = None
			unvisited.append(v)

		while len(unvisited) > 0:
			u = None

			for possibleU in unvisited:
				if u == None or dist[possibleU] < dist[u]:
					u = possibleU

			if u == target:
				break
				
			unvisited.remove(u)

			for v in u.neighbours:
				alt = dist[u] + self.calcualteDistance(v.x, v.y)
				if alt < dist[v]:
					dist[v] = alt
					prev[v] = u

		if prev[target] == None:
			return

		currentPath = []
		curr = target

		while curr != None:
			currentPath.append(curr)
			curr = prev[curr]

		currentPath.reverse()
		entity.currentPath = currentPath

	def calcualteDistance(self, x, y):
		if self.tiles["{0},{1}".format(x, y)].isPassable == False:
			return math.inf
		else:
			return 1


class Tile():
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type

		self.entity = None

		self.character = None

		self.isPassable = True

		self.visible = True

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, type):
		if type < 0 or type > 2:
			pass
		else:
			if type == 1:
				self.isPassable = False
			else:
				self.isPassable = True
			self.__type = type

	def __str__(self):
		if self.visible == False:
			return (" ")
		else:
			if self.type == 0:
				return "."
			elif self.type == 1:
				return "#"
			elif self.type == 2:
				return ">"
class Node():
	def __init__(self, x, y):
		self.neighbours = []
		self.x = x
		self.y = y
