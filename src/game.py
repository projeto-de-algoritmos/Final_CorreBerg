from map import Cells
import pygame
import constants as con
import os
from map import *
from player import Player
from enemy import Enemy
from coin import Coins

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(con.TITLE)
        self.surface = pygame.display.set_mode(
            (con.WINDOW_WIDTH, con.WINDOW_HEIGHT))
        self.BG_COLOR = con.BROWN
        self.keep_looping = True
        self.cells = Cells(self.surface)
        self.player = Player(self.surface, self.cells)
        self.enemy = Enemy(16, 14, self.surface, self.cells, self.player,con.PURPLE, 'player')
        self.enemyCoin = Enemy(15, 1, self.surface, self.cells, self.player, con.FUCHIA, 'coin')
        self.coins = Coins(self.surface, self.cells, self.player, self.enemy, self.enemyCoin)
        self.gameover = False

    def main(self):
        while self.keep_looping:
            self.draw()
            self.events()
            self.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                if event.key == pygame.K_RETURN:
                    self.cells.matrix[16][14].setType('p')
                if event.key == pygame.K_m:
                    self.cells.stroke = not self.cells.stroke
                if event.key == pygame.K_c:
                    self.enemy.showPath = not self.enemy.showPath
                    self.enemyCoin.showPath = not self.enemyCoin.showPath
                else:
                    # self.cells.printMap()
                    self.player.move(event, self.cells)

    def update(self):
        time_now = pygame.time.get_ticks()

        if time_now > self.enemy.last_movement + self.enemy.speed :
            self.enemy.moveTowardsPlayer('astar')
        if time_now > self.enemyCoin.last_movement + self.enemyCoin.speed :
            self.enemyCoin.moveTowardsCoin('astar', self.coins.closest)

        #self.gameOver()
        self.enemyCoin.getItem()
        self.player.getItem()
        self.coins.removePickedCoins()

    def draw(self):
        if (self.gameover == False):
            self.surface.fill(self.BG_COLOR)
            self.cells.draw()
            self.player.draw()
            self.enemy.draw()
            self.coins.draw()
            self.enemyCoin.draw()
            self.drawScore()
            

        # Testando limites
        # pygame.draw.rect(self.surface, con.YELLOW, self.cells.matrix[0][0])
        # pygame.draw.rect(self.surface, con.YELLOW, self.cells.matrix[19][19])

        pygame.display.update()

    def gameOver(self):
        if (self.enemy.x == self.player.x and self.enemy.y == self.player.y):
            self.gameover = True
            gameOverScreen = pygame.image.load(
                'src/images/gameover.png').convert_alpha()
            gameOverScreen = pygame.transform.scale(
                gameOverScreen, (con.WINDOW_WIDTH, con.WINDOW_HEIGHT))
            self.surface.blit(gameOverScreen, (0, 0))
    
    def restart(self):
        self.keep_looping = False
        jogo = Game()
        jogo.main()
    
    def drawScore(self):
        font = pygame.font.Font('freesansbold.ttf', 25)
        scorePlayer = font.render(f'SCORE: {int(self.player.points)}', True, (255, 255, 255))
        scoreEnemy = font.render(f'INIMIGO: {int(self.enemyCoin.points)}', True, (255, 255, 255))

        self.surface.blit(scorePlayer, (30, con.WINDOW_HEIGHT - 50))
        self.surface.blit(scoreEnemy, (con.WINDOW_WIDTH - 180, con.WINDOW_HEIGHT - 50))
