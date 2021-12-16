import os
import random

import pygame

WIDTH = 480
HEIGHT = 700
FPS = 60

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Самолёты")
clock = pygame.time.Clock()

ammo_event = pygame.USEREVENT + 1
pygame.time.set_timer(ammo_event, 10000)

heal_event = pygame.USEREVENT + 2
pygame.time.set_timer(heal_event, 20000)

ultimate_event = pygame.USEREVENT + 3
pygame.time.set_timer(ultimate_event, 30000)
ultimate_flag = False
ultimate_timeflag = False
ultimate_countdown = pygame.time.Clock()



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    # если файл не существует, то выходим
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


background = pygame.image.load('data/nebo.jpg').convert()
background = pygame.transform.smoothscale(background,
                                          screen.get_size())


class Player(pygame.sprite.Sprite):
    image = load_image('player_plane3.jpg', -1)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 70
        self.ammo = 10
        self.hp = 100
        self.count = 0
        self.speedx = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top + 75 > HEIGHT - 150:
            self.rect.top = HEIGHT - 225
        if self.rect.top < 0:
            self.rect.y = 0

    def shoot(self):
        if self.ammo > 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            if not ultimate_flag:
                self.ammo -= 1


class Mob(pygame.sprite.Sprite):
    image = load_image('enemy_mob_plane.jpg', -1)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        if self.rect.y >= 550:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet.jpg', -1)

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


class Ammos(pygame.sprite.Sprite):
    image = load_image('ammo.jpg', -1)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(100, HEIGHT - 150)


class Heals(pygame.sprite.Sprite):
    image = load_image('heal.jpg', -1)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(100, HEIGHT - 150)




all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ammos = pygame.sprite.Group()
heals = pygame.sprite.Group()
player = Player()
players = pygame.sprite.Group()
players.add(player)
all_sprites.add(player)


def draw():
    font = pygame.font.Font(None, 20)
    text = font.render("Снаряды", True, (255, 204, 0))
    text_x = 10
    text_y = 600
    screen.blit(text, (text_x, text_y))

    text_ammo = font.render(str(player.ammo), True, (255, 204, 0))
    text_y += 30
    screen.blit(text_ammo, (text_x, text_y))

    font = pygame.font.Font(None, 20)
    text = font.render("Здоровье", True, (255, 204, 0))
    text_x = 100
    text_y = 600
    screen.blit(text, (text_x, text_y))

    text_ammo = font.render(str(player.hp), True, (255, 204, 0))
    text_y += 30
    screen.blit(text_ammo, (text_x, text_y))

    font = pygame.font.Font(None, 20)
    text = font.render("Счёт", True, (255, 204, 0))
    text_x = 200
    text_y = 600
    screen.blit(text, (text_x, text_y))

    text_ammo = font.render(str(player.count), True, (255, 204, 0))
    text_y += 30
    screen.blit(text_ammo, (text_x, text_y))


for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Цикл игры
running = True
while running:
    screen.blit(background, (0, 0))
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        if event.type == ammo_event:
            if not ammos:
                am = Ammos()
                all_sprites.add(am)
                ammos.add(am)
        if event.type == heal_event:
            if not heals:
                he = Heals()
                all_sprites.add(he)
                heals.add(he)
        if event.type == ultimate_event:
            ultimate_timeflag = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                ultimate_flag = True
                ultimate_countdown = pygame.time.Clock()

    if ultimate_countdown.get_time() >= 10000:
        ultimate_flag = False

    if ultimate_flag:
        for i in range(10):
            player.shoot()

    # Обновление
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        player.count += 100

    hits = pygame.sprite.groupcollide(players, ammos, False, True)
    if hits:
        player.ammo += 10

    hits = pygame.sprite.groupcollide(players, heals, False, True)
    if hits:
        player.hp += 20


    if player.hp <= 0:
        running = False

    # Рендеринг
    screen.fill((0, 0, 0))
    draw()

    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        player.hp -= 20

    if not mobs:
        for i in range(5):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

pygame.quit()
