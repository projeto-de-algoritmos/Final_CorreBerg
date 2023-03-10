from algorithms import closest
import constants as con
import random
import pygame

class Coins:
	def __init__(self, surface, cells, player, enemy,enemyCoins):
		self.inner = []
		self.prohibited = []
		self.surface = surface
		self.cells = cells
		self.player = player
		self.enemy = enemy
		self.enemyCoins = enemyCoins
		self.closest = ()

		self.prohibited.append((self.player.x, self.player.y))
		self.prohibited.append((self.enemy.x, self.enemy.y))
		self.prohibited.append((self.enemyCoins.x, self.enemyCoins.y))
		self._generate_coins()
	
	def _generate_coins(self):
		for i in range(con.COINS_AMOUNT):
			x, y = 0, 0
			while self.cells.matrix[x][y].type not in 'g':
				x, y = random.randint(0, con.TILES_VERTICAL-1), random.randint(0, con.TILES_HORIZONTAL-1)
			if (x,y) not in self.prohibited:
				coin = Coin(x,y,self.cells.matrix[x][y])
				self.inner.append(coin)
				self.cells.matrix[x][y].items.append(coin)
				# Pesando as células das moedas para os inimigos não pegarem por acidente no A*
				self.cells.grid[x][y] = 200
				self.cells.matrix[x][y].weight = 200
		self.checkClosest()

	def draw(self):
		color = con.BLUE
		if len(self.inner) > 0:
			for coin in self.inner:
				if len(self.inner) > 2:
					if(self.closest[0][0] == coin.x and self.closest[0][1] == coin.y) or (self.closest[1][0] == coin.x and self.closest[1][1] == coin.y):
						color = con.BLUE
					else:
						color = con.DARK_RED
				pygame.draw.circle(self.surface, color, coin.cell.rect.center, 8)

	def removePickedCoins(self):
		for coin in self.inner:
			if coin.cell == None:
				self.inner.remove(coin)
		self.checkClosest()
	
	def checkClosest(self):
		coins = []
		for coin in self.inner:
			coins.append((coin.x,coin.y))
		if len(coins) > 1:
			self.closest = closest(coins)
		else:
			self.closest = coins

		



class Coin:
	def __init__(self, x, y, cell):
		self.x = x
		self.y = y
		self.value = con.COIN_VALUE
		self.cell = cell