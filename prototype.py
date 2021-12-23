import os
import random
import sys

import pygame

WIDTH = 480
HEIGHT = 700
FPS = 60
level_counter = 0
global_count = 0

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Самолёты")
clock = pygame.time.Clock()

seconds_counter_event = pygame.USEREVENT + 4
pygame.time.set_timer(seconds_counter_event, 1000)

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


class Background(pygame.sprite.Sprite):
    image = load_image('nebo.jpg')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Player(pygame.sprite.Sprite):
    image = load_image('player_plane.png', -1)
    image = pygame.transform.scale(image, (75, 75))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 70
        self.ammo = 10
        self.hp = 100
        self.speedx = 0
        self.speedy = 0

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
            self.ammo -= 1

    def special_shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    image = load_image('mob_plane.png', -1)
    image = pygame.transform.scale(image, (75, 75))

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
        if self.rect.top > HEIGHT + 10 or \
                self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        if self.rect.y >= 550:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet3.png', -1)
    image = pygame.transform.scale(image, (20, 40))

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


class EnemyBullet(pygame.sprite.Sprite):
    image = load_image('enemy_bullet.png', -1)
    image = pygame.transform.scale(image, (54, 100))

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.bottom = 240
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за нижнюю часть экрана
        if self.rect.bottom >= 550:
            self.kill()


class Ammos(pygame.sprite.Sprite):
    image = load_image('ammo.png', -1)
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(230,
                                       HEIGHT - 150 -
                                       self.rect.height)


class Heals(pygame.sprite.Sprite):
    image = load_image('heal1.png', -1)
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(230,
                                       HEIGHT - 150 -
                                       self.rect.height)


class Boss(pygame.sprite.Sprite):
    image = load_image('boss.png', -1)
    image = pygame.transform.scale(image, (480, 230))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.hp = 1000

    def update(self):
        if self.hp <= 0:
            self.kill()


screen.fill('black')

font = pygame.font.Font(None, 70)
game_name = font.render('Shump!', True, (255, 204, 0))
screen.blit(game_name, (150, 50))

intro_text = ['    В одной далёкой-далёкой галактике идёт война    ',
              'Вы отправились на фронт в качестве пилота космолёта.',
              'Сражайтесь с противником до самого конца и победите!']

font = pygame.font.Font(None, 24)
text_x = 10
text_y = 150
for line in intro_text:
    text = font.render(line, True, (255, 204, 0))
    screen.blit(text, (text_x, text_y))
    text_y += 40

instructions = ['                       Инструкции            ',
                'Управление космолётом - стрелочки',
                '   Стрельба из орудия - пробел   ',
                '   Специальная способность - E   ',
                '  Ультимативная способность - Q  ']

font = pygame.font.Font(None, 24)
text_x = 100
text_y = 400
for line in instructions:
    text = font.render(line, True, (204, 6, 5))
    screen.blit(text, (text_x, text_y))
    text_y += 40

next_text = 'Для того, чтобы начать игру, нажмите любую клавишу'
text_x = 25
text_y = 620
next_text = font.render(next_text, True, (199, 208, 204))
screen.blit(next_text, (text_x, text_y))

def starting():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


starting()
running_game = True
running_level = True

background = Background()

player = Player()
players = pygame.sprite.Group()
players.add(player)

ultimate_countdown = 0
ultimate_timer = 0
special_countdown = 0

ultimate_flag = False
ultimate_timeflag = False

special_flag = False
special_timeflag = False
shoots_counter = 0

time_to_boss = 120
time_to_heal = 20
time_to_ammo = 10


def draw():
    pygame.draw.rect(screen, 'black', [(0, 600), (WIDTH, HEIGHT)], 0)

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
    text_x = 130
    text_y = 600
    screen.blit(text, (text_x, text_y))

    text_ammo = font.render(str(player.hp), True, (255, 204, 0))
    text_y += 30
    screen.blit(text_ammo, (text_x, text_y))

    font = pygame.font.Font(None, 20)
    text = font.render("Счёт", True, (255, 204, 0))
    text_x = 270
    text_y = 600
    screen.blit(text, (text_x, text_y))

    text_ammo = font.render(str(global_count), True, (255, 204, 0))
    text_y += 30
    screen.blit(text_ammo, (text_x, text_y))

    font = pygame.font.Font(None, 20)
    text = font.render("Уровень", True, (255, 204, 0))
    text_x = 410
    text_y = 600
    screen.blit(text, (text_x, text_y))

    text_ammo = font.render(str(level_counter + 1),
                            True, (255, 204, 0))
    text_y += 30
    screen.blit(text_ammo, (text_x, text_y))

    if ultimate_timeflag or ultimate_flag:
        ult_color = (0, 255, 0)
    else:
        ult_color = (255, 0, 0)

    font = pygame.font.Font(None, 20)
    text = font.render("Ультимативная способность", True, ult_color)
    text_x = 10
    text_y = 650
    screen.blit(text, (text_x, text_y))

    if ultimate_timeflag:
        text_ult = 'Пуск!'
    else:
        if not ultimate_timeflag and not ultimate_flag:
            text_ult = f'{30 - ultimate_countdown}'
        if ultimate_flag:
            text_ult = f'{10 - ultimate_timer}'

    text_ult = font.render(str(text_ult), True, ult_color)
    text_x += 75
    text_y += 30
    screen.blit(text_ult, (text_x, text_y))

    if special_timeflag:
        spec_color = (0, 255, 0)
    else:
        spec_color = (255, 0, 0)

    font = pygame.font.Font(None, 20)
    text = font.render("Специальная способность", True, spec_color)
    text_x = 275
    text_y = 650
    screen.blit(text, (text_x, text_y))

    if special_timeflag:
        text_spec = 'Пуск!'
    else:
        if not special_timeflag:
            text_spec = f'{10 - special_countdown}'

    text_spec = font.render(str(text_spec), True, spec_color)
    text_x += 75
    text_y += 30
    screen.blit(text_spec, (text_x, text_y))


while running_game:
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    ammos = pygame.sprite.Group()
    heals = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    all_sprites.add(player)
    all_sprites.add(background)

    seconds_counter = 0
    heal_counter = 0
    ammo_counter = 0

    boss_flag = False
    boss_ap = False
    flag_enemy_shoot = False

    for i in range(8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Цикл игры
    while running_level:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                running_level = False
                running_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_q and ultimate_timeflag:
                    ultimate_flag = True
                    ultimate_timeflag = False
                if event.key == pygame.K_e and special_timeflag:
                    special_flag = True
            if event.type == seconds_counter_event:
                seconds_counter += 1
                if not ultimate_timeflag and not ultimate_flag:
                    ultimate_countdown += 1
                if ultimate_flag:
                    ultimate_timer += 1
                if not special_timeflag:
                    special_countdown += 1
                ammo_counter += 1
                heal_counter += 1
                flag_enemy_shoot = True

        if ultimate_countdown % 30 == 0 and ultimate_countdown != 0:
            ultimate_timeflag = True
            ultimate_countdown = 0

        if ultimate_flag:
            player.special_shoot()

        if ultimate_timer % 10 == 0 and ultimate_timer != 0:
            ultimate_timer = 0
            ultimate_flag = False

        if special_countdown % 10 == 0 and special_countdown != 0:
            special_timeflag = True
            special_countdown = 0

        if special_flag:
            player.special_shoot()
            if shoots_counter < 2:
                player.special_shoot()
                shoots_counter += 1
            else:
                shoots_counter = 0
                special_flag = False
            special_timeflag = False

        if ammo_counter % time_to_ammo == 0 and ammo_counter != 0:
            if not ammos:
                am = Ammos()
                all_sprites.add(am)
                ammos.add(am)

        if heal_counter % time_to_heal == 0 and heal_counter != 0:
            if not heals:
                he = Heals()
                all_sprites.add(he)
                heals.add(he)

        if seconds_counter >= time_to_boss:
            for mob in mobs:
                mob.kill()
            for obj in all_sprites:
                if isinstance(obj, Mob):
                    obj.kill()
            if not bosses and not boss_ap:
                boss = Boss()
                all_sprites.add(boss)
                bosses.add(boss)
                boss.hp += level_counter * 100
                boss_ap = True

        if seconds_counter % 10 == 0 and boss_ap and flag_enemy_shoot:
            if boss.hp > 0:
                xb = 0
                for i in range(3):
                    enemy_bullet = EnemyBullet(xb)
                    all_sprites.add(enemy_bullet)
                    enemy_bullets.add(enemy_bullet)
                    xb += 240
                xb = 0
                flag_enemy_shoot = False
        if boss_ap:
            if boss.hp <= 0:
                level_counter += 1
                running_level = False

        # Обновление
        all_sprites.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            global_count += 100

        hits = pygame.sprite.groupcollide(players, ammos, False, True)
        if hits:
            player.ammo += 10
            ammo_counter = 0

        hits = pygame.sprite.groupcollide(players, heals, False, True)
        if hits:
            player.hp += 20
            heal_counter = 0

        if player.hp <= 0:
            running_game = False
            running_level = False

        hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
        if hits:
            boss.hp -= 20
            global_count += 20

        hits = pygame.sprite.groupcollide(players, enemy_bullets,
                                          False, True)
        if hits:
            player.hp -= 20

        hits = pygame.sprite.groupcollide(players, bosses, False, False)
        if hits:
            player.hp -= 1
            boss.hp -= 5
            global_count += 5

        # Рендеринг
        screen.fill((0, 0, 0))

        all_sprites.draw(screen)
        players.draw(screen)
        draw()
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        # Проверка, не ударил ли моб игрока
        hits = pygame.sprite.spritecollide(player, mobs, True)
        if hits:
            global_count += 100
            player.hp -= 20

        if not mobs and not boss_flag:
            for i in range(5):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
    running_level = True
    time_to_boss += 10 * level_counter
    time_to_heal += 2 * level_counter
    time_to_ammo += 1 * level_counter
screen.fill('black')


def end_draw():
    screen.fill('black')

    font = pygame.font.Font(None, 70)
    game_name = font.render('Конец игры', True, (255, 204, 0))
    screen.blit(game_name, (100, 50))

    font = pygame.font.Font(None, 24)
    text = font.render('Счёт', True, (255, 204, 0))
    screen.blit(text, (80, 200))

    font = pygame.font.Font(None, 24)
    text = font.render(str(global_count), True, (255, 204, 0))
    screen.blit(text, (350, 200))

    font = pygame.font.Font(None, 24)
    text = font.render('Уровней пройдено', True, (255, 204, 0))
    screen.blit(text, (80, 300))

    font = pygame.font.Font(None, 24)
    text = font.render(str(level_counter + 1), True, (255, 204, 0))
    screen.blit(text, (350, 300))

    next_text = 'Для того, чтобы выйти из игры, нажмите пробел'
    text_x = 50
    text_y = 620
    next_text = font.render(next_text, True, (199, 208, 204))
    screen.blit(next_text, (text_x, text_y))


def ending():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


end_draw()
ending()
