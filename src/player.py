from coin import Coin
import constants as con
import pygame

class Player:
	def __init__(self, surface, cells):
		self.surface = surface
		self.cells = cells
		self.x = 8
		self.y = 17
		self.points = 0

	def draw(self):
		# Desenhando o player
		self.surface.fill(con.RED, pygame.Rect(self.x * con.TILESIZE, self.y * con.TILESIZE, con.TILESIZE, con.TILESIZE))

	def getItem(self, gameover, enemyCoin):
		items = self.cells.matrix[self.x][self.y].items
		if len(items) > 0:
			for item in items:
				if isinstance(item, Coin):
					item.cell = None
					items.remove(item)
			self.points += 1
			pygame.mixer.Sound.play(pygame.mixer.Sound("src/sounds/coin.mp3")).set_volume(0.5) if not gameover else 0
			enemyCoin.updateSpeed(20)


	def move(self, event, cells):
		# print(self.x, self.y)
		if event.key == pygame.K_w:
			if cells.getCell(self.x, self.y - 1).type in 'gbgb':
				self.y -= 1
		elif event.key == pygame.K_a:
			if cells.getCell(self.x - 1, self.y).type in 'gbgb':
				self.x -= 1
		elif event.key == pygame.K_s:
			if cells.getCell(self.x, self.y + 1).type in 'gbgb':
				self.y += 1
		elif event.key == pygame.K_d:
			if cells.getCell(self.x + 1, self.y).type in 'gbgb':
				self.x += 1