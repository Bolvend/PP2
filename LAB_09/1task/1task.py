#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINSCORE = 0
GETCOINSPEED = 5 #score that player need to reach to increase enemy speed
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK) 
background = pygame.image.load("AnimatedStreet.png")
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    # Settings for different coins
    coin_settings = {
            "gold": {"image": "goldcoin.png", "scale": 30, "score": 1},
            "silver": {"image": "goldcoin.png", "scale": 20, "score": 2},
            "diamond": {"image": "goldcoin.png", "scale": 10, "score": 5},
    }

    def __init__(self, coin_type="gold"):
        super().__init__()
        self.change_coin_type()
        self.rect = self.image.get_rect()
        self.reset()
        
    def change_coin_type(self):
        coin_type = random.choice(list(Coin.coin_settings.keys()))
        settings = Coin.coin_settings[coin_type]
        original_image = pygame.image.load(settings["image"])
        self.image = pygame.transform.scale(original_image, (settings["scale"], settings["scale"]))
        self.score_value = settings["score"]

    def reset(self):
        # New random coin position at the top of the screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-200, -50))
        self.change_coin_type()

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                   
#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    coinscores = font_small.render(str(COINSCORE), True, GOLD)
    DISPLAYSURF.blit(coinscores, (380,10))
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()


    #To be run if collision occurs between Player and Coin
    hit_coin = pygame.sprite.spritecollideany(P1, coins)
    if hit_coin:
        COINSCORE += hit_coin.score_value
        if COINSCORE >= GETCOINSPEED: #Increase the speed of Enemy when the player earns 5 coins
            SPEED += 1 
            GETCOINSPEED =  COINSCORE + 5
        pygame.mixer.Sound('pickupcoin.wav').play()
        hit_coin.reset()
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):	
          pygame.mixer.music.stop()
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()   
    
         
         
    pygame.display.update()
    FramePerSec.tick(FPS)