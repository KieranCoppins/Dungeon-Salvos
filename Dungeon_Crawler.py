#Kieran Coppins

import Interface
import Map
import Items
import Player
import Enemy
import Combat
import random

def equiptEventHandler(event, item):
	if event.keysym == "l":
		newPlayer.equipt("Left Hand", item)
	elif event.keysym == "r":
		newPlayer.equipt("Right Hand", item)
	
	UI.root.unbind("l")
	UI.root.unbind("r")
	UI.updateCharacterInfo(newPlayer)

def spawnPowerfulDude(event):
	print("Creating Chuck Norris")
	enemy = Enemy.Enemy("Chuck Norris", 9999999, 20, "C")
	startX = newPlayer.tile.x - 1
	endX = newPlayer.tile.x + 1

	startY = newPlayer.tile.y - 1
	endY = newPlayer.tile.y + 1

	for x in range(startX, endX + 1):
		for y in range(startY, endY + 1):
			keyword = "{0},{1}".format(x, y)
			tile = newMap.tiles[keyword]
			if tile.type == 0:
				enemy.setTile(newMap, tile.x, tile.y)

def equiptItem(item):
	id = item.identify()
	if id == "Weapon":
		returnVal = newPlayer.equiptItem(item)
		if returnVal != None:
			UI.printConsole("Equit {0} in [L]eft Hand or [R]ight Hand?\n".format(item.name))
			UI.root.bind("l", lambda event,  arg = item :  equiptEventHandler(event, arg))
			UI.root.bind("r", lambda event, arg = item : equiptEventHandler(event, arg))
	elif id == "Armour":
		newPlayer.equipt(item.slot, item)

def moveDownInv(event):
	if newPlayer.selectedItem == None:
		return

	index = newPlayer.inventory.index(newPlayer.selectedItem)
	if index + 1 <= len(newPlayer.inventory) - 1:
		newPlayer.selectedItem = newPlayer.inventory[index + 1]
	else:
		newPlayer.selectedItem = newPlayer.inventory[0]
	UI.updateInventory(newPlayer)

def moveUpInv(event):
	if newPlayer.selectedItem == None:
		return

	index = newPlayer.inventory.index(newPlayer.selectedItem)
	if index - 1 >= 0:
		newPlayer.selectedItem = newPlayer.inventory[index - 1]
	else:
		newPlayer.selectedItem = newPlayer.inventory[len(newPlayer.inventory)-1]
	UI.updateInventory(newPlayer)

def useItem(event):
	item = newPlayer.selectedItem
	if item == None:
		return

	id = item.identify()
	if id == "Consumable":
		item.consume(newPlayer)
	else:
		equiptItem(item)
	newPlayer.inventory.remove(item)
	if len(newPlayer.inventory) == 0:
		newPlayer.selectedItem = None
	else:
		newPlayer.selectedItem = newPlayer.inventory[0]
	UI.updateInventory(newPlayer)
	UI.updateCharacterInfo(newPlayer)

def destroyItem(event):
	item = newPlayer.selectedItem
	if item == None:
		return

	newPlayer.inventory.remove(item)
	if len(newPlayer.inventory) == 0:
		newPlayer.selectedItem = None
	else:
		newPlayer.selectedItem = newPlayer.inventory[0]
	UI.updateInventory(newPlayer)	

def movePlayerUp():
	newCoordX = newPlayer.tile.x - 1
	newCoordY = newPlayer.tile.y
	movePlayer(newCoordX, newCoordY)

def movePlayerDown():
	newCoordX = newPlayer.tile.x + 1
	newCoordY = newPlayer.tile.y
	movePlayer(newCoordX, newCoordY)
	
def movePlayerLeft():
	newCoordX = newPlayer.tile.x
	newCoordY = newPlayer.tile.y- 1
	movePlayer(newCoordX, newCoordY)
	
def movePlayerRight():
	newCoordX = newPlayer.tile.x
	newCoordY = newPlayer.tile.y + 1
	movePlayer(newCoordX, newCoordY)

def movePlayer(newCoordX, newCoordY):
	if newCoordX >= 0 and newCoordX < newMap.width and newCoordY >= 0 and newCoordY < newMap.height:
		if newMap.tiles["{0},{1}".format(newCoordX, newCoordY)].character != None:
			enemy = newMap.tiles["{0},{1}".format(newCoordX, newCoordY)].character
			initiateCombat(enemy)
		elif newMap.tiles["{0},{1}".format(newCoordX, newCoordY)].isPassable == True:
			newPlayer.setTile(newMap, newCoordX, newCoordY)
			if newMap.tiles["{0},{1}".format(newCoordX, newCoordY)].entity != None:
				newPlayer.pickUp(newMap.tiles["{0},{1}".format(newCoordX, newCoordY)].entity, newMap)
				UI.updateCharacterInfo(newPlayer)
			if newMap.tiles["{0},{1}".format(newCoordX, newCoordY)].type == 2:
				generateNewLevel()


def initiateCombat(enemy):
	newCombat = Combat.Combat(newPlayer, enemy)
	newCombat.runCombat(UI)

def updateFogOfWar():
	startX = newPlayer.tile.x - newPlayer.sightRange
	startY = newPlayer.tile.y - newPlayer.sightRange

	endX = newPlayer.tile.x + newPlayer.sightRange
	endY = newPlayer.tile.y + newPlayer.sightRange

	iX = startX
	iY = startY

	for iX in range(newMap.width):
		for iY in range(newMap.height):
			if iX < 0:
				iX = 0
			if iY < 0:
				iY = 0
			if iX >= newMap.width - 1:
				iX = newMap.width - 1
			if iY >= newMap.height - 1:
				iY = newMap.height - 1
			newMap.tiles["{0},{1}".format(iX, iY)].visible = False

	for iX in range(startX, endX):
		for iY in range(startY, endY):
			if iX < 0:
				iX = 0
			if iY < 0:
				iY = 0
			if iX >= newMap.width - 1:
				iX = newMap.width - 1
			if iY >= newMap.height - 1:
				iY = newMap.height - 1
			newMap.tiles["{0},{1}".format(iX, iY)].visible = True	

def updateEnemies():
	for enemy in enemies:
		if enemy.alive == False:
			enemies.remove(enemy)
		else:
			enemy.checkPlayer(newPlayer, newMap)
			combat = enemy.moveToNextTile(newMap, newPlayer)
			if combat != None:
				initiateCombat(enemy)

def endTurn(event):
	key = event.keysym

	if key == "Up":
		movePlayerUp()
	elif key == "Down":
		movePlayerDown()
	elif key == "Left":
		movePlayerLeft()
	elif key == "Right":
		movePlayerRight()

	updateEnemies()
	updateFogOfWar()
	newMap.displayMap(UI)
	UI.updateCharacterInfo(newPlayer)
	UI.updateInventory(newPlayer)

	UI.console.see("end")

	if newPlayer.alive == False:
		UI.createDeathScreen(level)

def generateNewLevel():
	global newMap
	global level
	level += 1
	itemlevelmodifier = 1 + (level*0.5)
	enemylevelmodifer = level * 2

	itemSpawnRateModifier = 1 + (level*0.1)
	enemySpawnRateModifer = 1 + (level*0.3)

	
	UI.root.title("Dungeon Salvos | Level: {0}".format(level))

	#Create the parameters for enemies, items here
	minEnemies = round(3 * enemySpawnRateModifer)
	maxEnemies = round(5 * enemySpawnRateModifer)

	numberOfEnemies = random.randint(minEnemies, maxEnemies)

	minItems = round(3 * itemSpawnRateModifier)
	maxItems = round(7 * itemSpawnRateModifier)

	numberOfItems = random.randint(minItems, maxItems)

	#global stat variables
	global enemiesStats
	global weapons
	global armour
	global consumables

	#Stores data of every enemy within the level
	global enemies

	enemies = []
	

	newMap = Map.Map(40, 100, 10, 3, 4, 8)
	newMap.generateDungeon()
	placePlayer()

	#Create enemies and place them randomly
	for i in range(numberOfEnemies):
		randomEnemyIndex = random.randint(0, len(enemiesStats) - 1)
		enemyStats = enemiesStats[randomEnemyIndex]
		name = enemyStats[0]
		health = enemyStats[1]
		damage = enemyStats[2]
		graphic = enemyStats[3]

		health = round(health * enemylevelmodifer)
		damage = round(damage * enemylevelmodifer)
		print("Creating enemy {0}".format(name))
		newEnemy = Enemy.Enemy(name, health, damage, graphic)
		emptyTile = newMap.getEmptyTile()
		newEnemy.setTile(newMap, emptyTile.x, emptyTile.y)
		enemies.append(newEnemy)

	for i in range(numberOfItems):
		itemTypeChance = random.randint(1, 5)
		itemRarity = random.randint(1, 10)	#60% chance of tier 1, 30% chance of tier 2, 10% chance of tier 3

		if itemTypeChance == 5:
			#spawn consumable
			if itemRarity == 10:
				itemStats = consumables[2]
			elif itemRarity <= 6:
				itemStats = consumables[0]
			else:
				itemStats = consumables[1]
			name = itemStats[0]
			stat = itemStats[1]
			modifier = itemStats[2]
			modifier = round(modifier * itemlevelmodifier)
			item = Items.Consumable(name, stat, modifier)

		elif itemTypeChance <= 2:
			#spawn weapon
			if itemRarity == 10:
				itemStats = weapons[2]
			elif itemRarity <= 6:
				itemStats = weapons[0]
			else:
				itemStats = weapons[1]

			randomItem = random.randint(0, len(itemStats) - 1)
			itemStats = itemStats[randomItem]
			minDamage = itemStats[0]
			maxDamage = itemStats[1]
			name = itemStats[2]
			minDamage = round(minDamage * itemlevelmodifier)
			maxDamage = round(maxDamage * itemlevelmodifier)
			item = Items.Weapon(minDamage, maxDamage, name)
		else:
			#spawn armour
			if itemRarity == 10:
				itemStats = armour[2]
			elif itemRarity <= 6:
				itemStats = armour[0]
			else:
				itemStats = armour[1]

			randomItem = random.randint(0, len(itemStats) - 1)
			itemStats = itemStats[randomItem]
			name = itemStats[0]
			defence = itemStats[1]
			slot = itemStats[2]
			defence = round(defence * itemlevelmodifier)
			item = Items.Armour(name, defence, slot)

		emptyTile = newMap.getEmptyTile()
		emptyTile.entity = item


def placePlayer():
	global newPlayer
	global newMap
	emptyTile = newMap.getEmptyTile()
	newPlayer.setTile(newMap, emptyTile.x, emptyTile.y)

def createCharacter(name):
	global newPlayer
	newPlayer = Player.Player(name)
	newPlayer.equipt("Head", Items.Armour("Nothing", 0, "Head"))
	newPlayer.equipt("Chest", Items.Armour("Nothing", 0, "Chest"))
	newPlayer.equipt("Legs", Items.Armour("Nothing", 0, "Legs"))
	newPlayer.equipt("Left Hand", Items.Weapon(1, 5, "Fist"))
	newPlayer.equipt("Right Hand", Items.Weapon(1, 5, "Fist"))

#global vars that are needed throughout the program
newMap = None
newPlayer = None
level = 0

enemies = []
enemiesStats = []
weapons = [[],[],[]]
armour = [[],[],[]]
consumables = []

#create another list within the enemies list making a 2d list of base variables for each enemy type
#some values maybe modified depending on floor level
#enemies.append([name, health, damage, graphic])

enemiesStats.append(["Frail Goblin", 6, 5, "G"])
enemiesStats.append(["Strong Orc", 13, 8, "O"])
enemiesStats.append(["Zombie", 3, 6, "Z"])
enemiesStats.append(["Dark Elf", 10, 6, "E"])

#create another list within the weapons list making a 2d list of base variables for each weapon type
#some values maybe modified depending on floor level
#weapons.append([minDamage, maxDamage, name])
#melee is the only combat type in this game, therefore weapons will include, swords, spears, symitars etc
#IF we stick with the template of:
#Swords deal moderate min and max damage
#Symitars deal low min but high max damages
#Spears hit high min but low max damages
#Three metal tiers: Iron (1), Aluminium(2), Steel (3)

weapons[0].append([2, 6, "Bronze Sword"])
weapons[0].append([1, 8, "Bronze Scimitar"])
weapons[0].append([3, 4, "Bronze Spear"])

weapons[1].append([5, 10, "Iron Sword"])
weapons[1].append([3, 12, "Iron Scimitar"])
weapons[1].append([6, 8, "Iron Spear"])

weapons[2].append([8, 13, "Steel Sword"])
weapons[2].append([6, 17, "Steel Scimitar"])
weapons[2].append([9, 11, "Steel Spear"])

#create another list within the armour list making a 2d list of base variables for each armour type
#some values maybe modified depending on floor level
#armour.append([name, defence, slot])
#Order is most defence -> Chest, Legs, Helmet

armour[0].append(["Bronze Helmet", 1, "Head"])
armour[0].append(["Bronze Chest", 5, "Chest"])
armour[0].append(["Bronze Legs", 3, "Legs"])

armour[1].append(["Iron Helmet", 3, "Head"])
armour[1].append(["Iron Chest", 8, "Chest"])
armour[1].append(["Iron Legs", 6, "Legs"])

armour[2].append(["Steel Helmet", 5, "Head"])
armour[2].append(["Steel Chest", 12, "Chest"])
armour[2].append(["Steel Legs", 8, "Legs"])

#create another list within the consumables list making a 2d list of base variables for each consumable type
#some values maybe modified depending on floor level
#consumables.append([name, stat, modifier])
#in this game only stat is health but others can be modified in the future

consumables.append(["Bandages", "Health", 3])
consumables.append(["Medicine", "Health", 7])
consumables.append(["Life Potion", "Health", 12])

#On startup create UI and first map and first instance of the player
UI = Interface.Interface()
name = input("Please enter a name for your character: ")
createCharacter(name)
generateNewLevel()
UI.updateCharacterInfo(newPlayer)
UI.updateInventory(newPlayer)
updateFogOfWar()
newMap.displayMap(UI)

#Set up Button Binds
UI.root.bind("<Up>", endTurn)
UI.root.bind("<Down>", endTurn)
UI.root.bind("<Left>", endTurn)
UI.root.bind("<Right>", endTurn)
UI.root.bind("[", moveUpInv)
UI.root.bind("]", moveDownInv)
UI.root.bind("<Return>", useItem)
UI.root.bind("<BackSpace>", destroyItem)
UI.root.bind("<space>", endTurn)

UI.root.title("Dungeon Salvos | Level: {0}".format(level))

#UI.root.bind("<p>", spawnPowerfulDude)

#Pack the UI
UI.mainframe.pack()
UI.mainframe.focus_set()
UI.root.mainloop()
