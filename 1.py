from pygame import *
from random import randint

font.init()
font1 = font.Font(None, 36)

# Archivos
img_ast = "asteroid.png"
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

# Variables del juego
score = 0
lost = 0
max_lost = 3
goal = 10
life = 3
rel_time = False
num_fire = 0

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Tirador")
background = transform.scale(image.load(img_back), (win_width, win_height))

# Clase base
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Jugador
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        fire_sound.play()

# Enemigos
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

# Balas
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Grupos
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


# Música
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

# Juego
run = True
finish = False
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        # Colisiones
        collisions = sprite.groupcollide(monsters, bullets, True, True)
        for c in collisions:
            score += 1
            new_enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(new_enemy)

            if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
               sprite.spritecollide(ship, monsters, True)
               sprite.spritecollide(ship, asteroids, True)
               life = life -1

            if life == 0 or lost >= max_lost:
                finish = True
                window.blit(lost, (200, 200))

        # Puntajes
        text = font1.render("Puntaje: " + str(score), True, (255, 255, 255))
        text_lose = font1.render("Fallados: " + str(lost), True, (255, 255, 255))
        window.blit(text, (10, 20))
        window.blit(text_lose, (10, 50))

        if lost >= max_lost:
            finish = True
            lose_text = font1.render("¡PERDISTE!", True, (255, 0, 0))
            window.blit(lose_text, (250, 250))
        elif score >= goal:
            finish = True
            win_text = font1.render("¡GANASTE!", True, (0, 255, 0))
            window.blit(win_text, (250, 250))

        display.update()
        clock.tick(60)
