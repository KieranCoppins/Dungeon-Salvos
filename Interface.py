#Kieran Coppins

import tkinter as TK

class Interface():
	def __init__(self):
		self.root = TK.Tk()
		self.mainframe = TK.Frame(self.root)

		#Text Based map design - using characters to represent tiles.
		self.map = TK.Text(self.mainframe, width = 100, height = 40)
		self.map.grid(row = 1, rowspan = 2, column = 1)

		self.map.tag_configure("default", background="black", foreground="white")
		self.map.tag_configure("player", background="black", foreground="blue")
		self.map.tag_configure("enemy", background="black", foreground="red")
		self.map.tag_configure("armour", background="black", foreground="cyan")
		self.map.tag_configure("weapon", background="black", foreground="magenta")
		self.map.tag_configure("consumable", background="black", foreground="yellow")

		self.console = TK.Text(self.mainframe, width = 100, height = 10, background="black", foreground="white")
		self.console.grid(row = 3, column = 1)

		self.characterInfo = TK.Text(self.mainframe, width = 50, height = 20, background="black", foreground="white")
		self.characterInfo.grid(row = 1, column = 2)

		self.characterInfo.tag_configure("red", background="black", foreground="red")
		self.characterInfo.tag_configure("yellow", background="black", foreground="yellow")
		self.characterInfo.tag_configure("green", background="black", foreground="green")

		self.inventory = TK.Text(self.mainframe, width = 50, height = 20, background="black", foreground="white")
		self.inventory.grid(row = 2, column = 2)

		self.stats = TK.Text(self.mainframe, width = 50, height = 10, background="black", foreground="white")
		self.stats.grid(row = 3, column = 2)

		self.map.config(state="disabled")
		self.console.config(state="disabled")
		self.characterInfo.config(state="disabled")
		self.inventory.config(state="disabled")
		self.stats.config(state="disabled")

	def clearMap(self):
		self.map.config(state="normal")
		self.map.delete(0.0, TK.END)
		self.map.config(state="disabled")
	
	def clearConsole(self):
		self.console.config(state="normal")
		self.console.delete(0.0, TK.END)
		self.console.config(state="disabled")

	def clearCharacterInfo(self):
		self.characterInfo.config(state="normal")
		self.characterInfo.delete(0.0, TK.END)
		self.characterInfo.config(state="disabled")

	def clearInventory(self):
		self.inventory.config(state="normal")
		self.inventory.delete(0.0, TK.END)
		self.inventory.config(state="disabled")

	def clearStats(self):
		self.stats.config(state="normal")
		self.stats.delete(0.0, TK.END)
		self.stats.config(state="disabled")


	#text based print map
	def printMap(self, string, tag = "default"):
		self.map.insert(TK.END, string, tag)

	def printConsole(self, string):
		self.console.config(state="normal")
		self.console.insert(TK.END, string, "default")
		self.console.config(state="disabled")

	def printCharacterInfo(self, string):
		self.characterInfo.config(state="normal")
		self.characterInfo.insert(TK.END, string, "default")
		self.characterInfo.config(state="disabled")

	def printInventory(self, string):
		self.inventory.config(state="normal")
		self.inventory.insert(TK.END, string, "default")
		self.inventory.config(state="disabled")

	def printStats(self, string):
		self.stats.config(state="normal")
		self.stats.insert(TK.END, string, "default")
		self.stats.config(state="disabled")

	def updateCharacterInfo(self, player):
		self.clearCharacterInfo()
		self.characterInfo.config(state="normal")
		self.characterInfo.insert(TK.END, "[Character Information] \n")
		self.characterInfo.insert(TK.END, "[Name] {0} \n".format(player.name))
		self.characterInfo.insert(TK.END, "[Health] ")
		if player.health <= 33:
			tag = "red"
		elif player.health <= 66:
			tag = "yellow"
		else:
			tag = "green"
		self.characterInfo.insert(TK.END, "{0:10} ".format(player.generateHealthBar()), tag)
		self.characterInfo.insert(TK.END, "{0:3}/{1:3}\n".format(player.health, 100))
		minDmg, maxDmg = player.calculateDamage()
		self.characterInfo.insert(TK.END, "[Damage] {0}-{1}\n".format(minDmg, maxDmg))
		defence = player.calculateDefence()
		self.characterInfo.insert(TK.END, "[Defence] {0}\n".format(defence))
		self.characterInfo.insert(TK.END, "[Equiptment]\n")
		self.characterInfo.insert(TK.END, "[Head] {0}({1})\n".format(player.items["Head"].name, player.items["Head"].defence))
		self.characterInfo.insert(TK.END, "[Chest] {0}({1})\n".format(player.items["Chest"].name, player.items["Chest"].defence))
		self.characterInfo.insert(TK.END, "[Legs] {0}({1})\n".format(player.items["Legs"].name, player.items["Legs"].defence))
		self.characterInfo.insert(TK.END, "[Left Hand] {0}({1}-{2})\n".format(player.items["Left Hand"].name, player.items["Left Hand"].minDamage, player.items["Left Hand"].maxDamage))
		self.characterInfo.insert(TK.END, "[Right Hand] {0}({1}-{2})\n".format(player.items["Right Hand"].name, player.items["Right Hand"].minDamage, player.items["Right Hand"].maxDamage))
		
		self.characterInfo.config(state="disabled")

	def updateInventory(self, player):
		self.clearInventory()
		self.inventory.config(state="normal")
		self.inventory.insert(TK.END, "[Inventory]\n", "default")
		for item in player.inventory:
			id = item.identify()
			if id == "Weapon":
				itemFormat = "{0}({1}-{2})".format(item.name, item.minDamage, item.maxDamage)
			elif id == "Armour":
				itemFormat = "{0}({1})".format(item.name, item.defence)
			else:
				itemFormat = "{0}({1}+{2})".format(item.name, item.stat, item.modifier)
			if item == player.selectedItem:
				self.inventory.insert(TK.END, "[{0}]-Selected\n".format(itemFormat), "default")
			else:
				self.inventory.insert(TK.END, "{0}\n".format(itemFormat), "default")
		self.inventory.config(state="disabled")

	def quitGame(self):
		self.root.destroy()

	def createDeathScreen(self, level):
		self.mainframe.destroy()
		self.deathFrame = TK.Frame(self.root)
		self.deathMessageLine1 = TK.Label(self.deathFrame, text = "Game Over, Player's Health Depleated")
		self.deathMessageLine2 = TK.Label(self.deathFrame, text = "You made it to level {0}".format(level))
		self.deathMessageLine1.grid(row = 1, column = 1)
		self.deathMessageLine2.grid(row = 2, column = 1)

		self.closeGameButton = TK.Button(self.deathFrame, text = "Quit", command = self.quitGame)
		self.closeGameButton.grid(row = 3, column = 1)

		self.deathFrame.pack()
