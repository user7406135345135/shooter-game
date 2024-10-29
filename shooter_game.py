from pygame import *
from random import *
from time import time as timer

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, speed, size_x, size_y, texture, is_asteroid = False):
        super().__init__()
        self.image = transform.scale(image.load(texture), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_asteroid = is_asteroid
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class PLayer(GameSprite):
    def update(self):
        k = key.get_pressed()
        if k[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if k[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(self.rect.x + 33, self.rect.y, 15, 15, 20, 'bullet.png')
        bullets.add(bullet)
        fire.play()

lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = -50
            self.rect.x = randint(0, win_width - 80)        
            self.speed = 1+random()
            if not self.is_asteroid:
                lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()         
mixer.init()
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
#mixer.music.play()

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy(randint(0, win_width-80), -50, 1+random(), 80, 50, 'ufo.png')
    monsters.add(monster)

for k in range(3):
    asteroid = Enemy(randint(0, win_width - 80), -50, 1+random(), 80, 50, 'asteroid.png', True)
    asteroids.add(asteroid)

player = PLayer(350, 400, 10, 80, 100, 'rocket.png')

rel_time = False
num_fire = 0


font.init()
font1 = font.SysFont('Arial', 20)
font2 = font.SysFont('Arial', 20)
font3 = font.SysFont('Arial', 100)
font4 = font.SysFont('Arial', 100)
font5 = font.SysFont('Arial', 70)
font6 = font.SysFont('Arial', 50)
win = font3.render('YOU WIN', True, (255, 200, 0))
lose = font4.render('YOU LOSE', True, (255, 0, 0))


lifes = 3
finish = False
clock = time.Clock()
game = True
while game:
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.show()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        text_lost = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_scores = font1.render('Счет: ' + str(score), 1, (255, 255, 255))
        if lifes == 3:
            color = (200, 255, 200)
        elif lifes == 2:
            color = (255, 255, 0)
        elif lifes == 1:
            color = (255, 0, 0)
        text_lifes = font5.render(str(lifes), 1, color)
        window.blit(text_lifes, (650, 30))
        window.blit(text_scores, (0, 15))
        window.blit(text_lost, (0, 30))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font6.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            lifes -= 1
        if lost >= 3 or lifes <= 0:
            window.blit(lose, (200, 200))
            finish = True
        sprites_list1 = sprite.groupcollide(asteroids, bullets, False, True)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprites_list:
            score += 1
            monster = Enemy(randint(0, win_width-80), -50, randint(2,4), 80, 50, 'ufo.png')
            monsters.add(monster)
            if score >= 10:
                window.blit(win, (200, 200))
                finish = True
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    display.update()    
    clock.tick(40)
