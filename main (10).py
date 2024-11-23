import pygame, sys
from pygame.locals import QUIT
import time
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (125, 125, 125)
ENEMYGREY = (160, 160, 160)
LIGHTGREY = (200, 200, 200)
SHOPGREY = (210, 210, 210)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
PURPLE = (200, 0, 255)
BACK = (230, 230, 255)
SKY = (175, 200, 255)
SPOT = (200, 255, 200)

clock = pygame.time.Clock()

background = pygame.Rect(0, 0, 700, 350)
tower = pygame.Rect(600, 75, 75, 125)

towerHP = 3000

enemy = pygame.Rect(-100, 175, 20, 20)

path1 = pygame.Rect(0, 155, 200, 40)
path2 = pygame.Rect(200, 20, 40, 175)
path3 = pygame.Rect(240, 20, 80, 40)
path4 = pygame.Rect(320, 20, 40, 310)
path5 = pygame.Rect(360, 290, 80, 40)
path6 = pygame.Rect(440, 155, 40, 175)
path7 = pygame.Rect(480, 155, 120, 40)

spot1 = pygame.Rect(100, 90, 50, 50)
spot2 = pygame.Rect(100, 210, 50, 50)
spot3 = pygame.Rect(255, 70, 50, 50)
spot4 = pygame.Rect(375, 230, 50, 50)
spot5 = pygame.Rect(500, 90, 50, 50)
spot6 = pygame.Rect(500, 210, 50, 50)

spot1used = False
spot2used = False
spot3used = False
spot4used = False
spot5used = False
spot6used = False

buying = False
purchased = ""

shoparea = pygame.Rect(0, 270, 300, 230)

sword1 = pygame.image.load("Defenders/sword1.png")
sword1 = pygame.transform.scale(sword1, (50, 50))
sword2 = pygame.image.load("Defenders/sword2.png")
sword2 = pygame.transform.scale(sword2, (50, 50))

enemyTimer = 0
enemyTimerLimit = 500
enRand1 = 1300
enRand2 = 1700

enemyFTimer = 0
enemyFTimerLimit = 3000
fnRand1 = 2500
fnRand2 = 3500

enemyHeavTimer = 0
enemyHeavTimerLimit = 7500

swordtime = 0

gold = 50

font = pygame.font.Font('freesansbold.ttf', 32)
goldtxt = font.render("Gold: " + str(gold), True, YELLOW, GREEN)
goldtxtRect = goldtxt.get_rect()
goldtxtRect.center = (75, 25)
towtxt = font.render("Tower HP: " + str(towerHP), True, BLACK, GREEN)
towtxtRect = towtxt.get_rect()
towtxtRect.center = (550, 25)

font2 = pygame.font.Font('freesansbold.ttf', 16)
sword1cost = font2.render("50 G", True, YELLOW, SHOPGREY)
sword1costRect = sword1.get_rect()
sword1costRect.center = (50, 360)
sword2cost = font2.render("150 G", True, YELLOW, SHOPGREY)

shop = font2.render("SHOP", True, BLACK, SHOPGREY)
shopRect = shop.get_rect()
shopRect.center = (150, 285)

DISPLAYSURF = pygame.display.set_mode((700, 350))
pygame.display.set_caption('Tower Defense')


class Enemy():
    # Drops 25 Gold
    def __init__(self):
        # Red
        self.rect = pygame.Rect(-100, 163, 20, 20)
        self.x = -999
        self.y = 163
        self.speed = 0.1
        self.hp = 2
        self.checkpoint = False
        self.checkpoint2 = False
        self.color = RED
        self.dead = False
        self.g = 25

    def move(self, x, y):
      if self.x != -999:
        if not self.checkpoint and not self.checkpoint2:
            if x < 210:
                self.x += self.speed
            else:
                if y > 30:
                    self.y -= self.speed
                else:
                    self.checkpoint = True
        elif self.checkpoint and not self.checkpoint2:
            if x < 330:
                self.x += self.speed
            else:
                if y < 300:
                    self.y += self.speed
                else:
                    self.checkpoint2 = True
        else:
            if x < 450:
                self.x += self.speed
            else:
                if y > 165:
                    self.y -= self.speed
        if x >= 450 and y <= 165 and x <= 580:
            self.x += self.speed

    def die(self):
        global gold
        self.speed = 0
        self.dead = True
        gold += self.g

    def spawn(self):
      newEnemy = Enemy()
      enemyList.append(newEnemy)
      newEnemy.x = -100
      newEnemy.y = 163
  
    def draw(self):
        if self.dead == False:
            self.rect = pygame.Rect(self.x, self.y, 20, 20)
            pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
            if self.hp <= 0:
                self.die()

    def attack(self):
      global towerHP
      if self.dead == False:
        towerHP -= 1


class FastEnemy(Enemy):
    # Drops 25 Gold
    def __init__(self):
        # Blue
        self.rect = pygame.Rect(-100, 163, 20, 20)
        self.x = -999
        self.y = 163
        self.speed = 0.3
        self.hp = 1
        self.checkpoint = False
        self.checkpoint2 = False
        self.color = BLUE
        self.dead = False
        self.g = 25

    def spawn(self):
      newFEnemy = FastEnemy()
      enemyFList.append(newFEnemy)
      newFEnemy.x = -100
      newFEnemy.y = 163
    
    def draw(self):
      if self.dead == False:
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
        if self.hp <= 0:
          self.die()


class HeavyEnemy(Enemy):
    # Drops 50 Gold
    def __init__(self):
        # Grey
        self.rect = pygame.Rect(-100, 163, 20, 20)
        self.x = -999
        self.y = 163
        self.speed = 0.05
        self.hp = 3
        self.checkpoint = False
        self.checkpoint2 = False
        self.color = ENEMYGREY
        self.g = 50

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(DISPLAYSURF, self.color, self.rect)


class HackerEnemy(Enemy):
    # Drops 25 Gold
    def __init__(self):
        # Dark Green, can destroy turrets
        self.rect = pygame.Rect(-100, 175, 20, 20)
        self.x = -999
        self.y = 163
        self.speed = 0.08
        self.hp = 1
        self.g = 25


class BossEnemy(Enemy):
    # Drops 100 Gold
    def __init__(self):
        # Purple
        self.rect = pygame.Rect(-50, 175, 30, 30)
        self.x = -50
        self.y = 163
        self.speed = 0.02
        self.hp = 50
        self.g = 100


class Melee():
    # Costs 50 Gold
    def __init__(self):
        self.image = pygame.image.load('Defenders/sword1.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = pygame.Rect(200, -100, 50, 50)
        self.x = -999
        self.y = -999
        self.swordtime = 0
        self.speed = 300

    def attack(self, target):
        target.hp -= 1

    def spawn(self, xpoint, ypoint):
        newMelee = Melee()
        meleeList.append(newMelee)
        newMelee.x = xpoint
        newMelee.y = ypoint

    def die(self):
        pass

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, 25, 25)
        DISPLAYSURF.blit(self.image, (self.x, self.y))


enemy = Enemy()
fastEnemy = FastEnemy()
heavyEnemy = HeavyEnemy()
melee = Melee()
meleeList = []
enemyList = []
enemyFList = []

while True:
    #print(towerHP)
    pygame.draw.rect(DISPLAYSURF, GREEN, background)
    pygame.draw.rect(DISPLAYSURF, GREY, tower)
    pygame.draw.rect(DISPLAYSURF, LIGHTGREY, path1)
    pygame.draw.rect(DISPLAYSURF, LIGHTGREY, path2)
    pygame.draw.rect(DISPLAYSURF, LIGHTGREY, path3)
    pygame.draw.rect(DISPLAYSURF, LIGHTGREY, path4)
    pygame.draw.rect(DISPLAYSURF, LIGHTGREY, path5)
    pygame.draw.rect(DISPLAYSURF, LIGHTGREY, path6)
    pygame.draw.rect(DISPLAYSURF, LIGHTGREY, path7)
    pygame.draw.rect(DISPLAYSURF, SPOT, spot1)
    pygame.draw.rect(DISPLAYSURF, SPOT, spot2)
    pygame.draw.rect(DISPLAYSURF, SPOT, spot3)
    pygame.draw.rect(DISPLAYSURF, SPOT, spot4)
    pygame.draw.rect(DISPLAYSURF, SPOT, spot5)
    pygame.draw.rect(DISPLAYSURF, SPOT, spot6)
    pygame.draw.rect(DISPLAYSURF, SHOPGREY, shoparea)
    for ene in enemyList:
      ene.draw()
      ene.move(ene.x, ene.y)
      if ene.x >= 580:
        ene.attack()
    for enef in enemyFList:
      enef.draw()
      enef.move(enef.x, enef.y)
      if enef.x >= 580:
        enef.attack()
    goldtxt = font.render("Gold: " + str(gold), True, YELLOW, GREEN)
    towtxt = font.render("Tower HP: " + str(towerHP), True, BLACK, GREEN)
    sword1cost = font2.render("50 G", True, YELLOW, SHOPGREY)
    DISPLAYSURF.blit(goldtxt, goldtxtRect)
    DISPLAYSURF.blit(towtxt, towtxtRect)
    DISPLAYSURF.blit(shop, shopRect)
    sword1Rect = sword1.get_rect()
    sword1Rect.center = (55, 305)
    pygame.draw.rect(DISPLAYSURF, SHOPGREY, sword1Rect)
    DISPLAYSURF.blit(sword1, (30, 280))
    DISPLAYSURF.blit(sword1cost, sword1costRect)
    enemyTimer += 1
    enemyFTimer += 1
    enemyHeavTimer += 1
    if enemyTimer >= enemyTimerLimit:
      enemy.spawn()
      enemyTimer = 0
      enemyTimerLimit = random.randint(enRand1, enRand2)
      if enRand1 > 300:
        enRand1 -= 50
        enRand2 -= 50
    if enemyFTimer >= enemyFTimerLimit:
      fastEnemy.spawn()
      enemyFTimer = 0
      enemyFTimerLimit = random.randint(fnRand1, fnRand2)
      if fnRand1 > 800:
        fnRand1 -= 50
        fnRand2 -= 50
    
    #print(swordtime)
    for item in meleeList:
      item.draw()
      item.swordtime += 1
      if item.swordtime >= 500:
        for item2 in enemyList:
            if item2.x >= item.x - 30 and item2.x <= item.x + 30:
                item.attack(item2)
            elif item2.y >= item.y - 30 and item2.y <= item.y + 30:
                item.attack(item2)
        for item3 in enemyFList:
            if item3.x >= item.x - 30 and item3.x <= item.x + 30:
                item.attack(item3)
            elif item3.y >= item.y - 30 and item3.y <= item.y + 30:
                item.attack(item3)
        item.swordtime = 0

    if towerHP <= 0:
      print("GAME OVER")
      pygame.quit()
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if sword1Rect.collidepoint(pos):
              if gold >= 50:
                buying = True
                purchased = "sword1"
            if spot1.collidepoint(pos) and spot1used == False:
              if buying == True:
                if purchased == "sword1":
                  melee.spawn(100, 90)
                  gold -= 50
                  buying = False
            if spot2.collidepoint(pos) and spot2used == False:
              if buying == True:
                if purchased == "sword1":
                  melee.spawn(100, 210)
                  gold -= 50
                  buying = False
            if spot3.collidepoint(pos) and spot3used == False:
              if buying == True:
                if purchased == "sword1":
                  melee.spawn(255, 70)
                  gold -= 50
                  buying = False
            if spot4.collidepoint(pos) and spot4used == False:
              if buying == True:
                if purchased == "sword1":
                  melee.spawn(375, 230)
                  gold -= 50
                  buying = False
            if spot5.collidepoint(pos) and spot5used == False:
              if buying == True:
                if purchased == "sword1":
                  melee.spawn(500, 90)
                  gold -= 50
                  buying = False
            if spot6.collidepoint(pos) and spot6used == False:
              if buying == True:
                if purchased == "sword1":
                  melee.spawn(500, 210)
                  gold -= 50
                  buying = False
    
      if event.type == QUIT:
          pygame.quit()
          sys.exit()
    pygame.display.update()
    clock.tick(300)
