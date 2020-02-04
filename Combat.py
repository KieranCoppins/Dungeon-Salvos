#Kieran Coppins

class Combat():
	def __init__(self, player, enemy):
		self.player = player
		self.enemy = enemy

	def calcualteHits(self):
		playerHit = self.player.calculateHit(self.enemy.damage)
		enemyHit = self.player.getHitDamage()
		self.enemy.health -= enemyHit
		return playerHit, enemyHit

	def runCombat(self, UI):
		playerHit, enemyHit = self.calcualteHits()
		UI.printConsole("{0} hit {1} for {2} damage, {1} now has {3} health\n".format(self.player.name, self.enemy.name, enemyHit, self.enemy.health))
		UI.printConsole("{0} hit {1} for {2} damage, {1} now has {3} health\n".format(self.enemy.name, self.player.name, playerHit, self.player.health))

