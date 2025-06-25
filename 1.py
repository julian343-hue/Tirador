from pygame import *
from random import randint

font.init()
font1 = font.Font(None, 36)

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
number = 0
lost = 0
clock = 60
score = 0
bullet = 0
score = 0 
max_lost = 3 

win_width = 700
win_height = 500
display.set_caption("Tirador")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullet.add(bullet)        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Tirador")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


text_lose = font1.render(
    "Fallados:" + str(lost), 1, (255, 255, 255)
)
    
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.music.load("fire.ogg")

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:

        window.blit(background, (0, 0))
        text = font1.render("Puntaje: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font1.render("Fallados: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        ship.update()
        monsters.update()
        bullet.Update()


        ship.reset()
        bullet.reset()

        display.update()

        monsters.draw(window)
        monsters.update()
        bullet.draw(window)

    time.delay(clock)

