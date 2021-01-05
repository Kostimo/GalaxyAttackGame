'''Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3'''
import pygame
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60

score_list = [500, 1000, 2000, 5000, 7500, 10000, 15000, 20000]


# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE_100 = (255, 255, 255)
WHITE_90 = (230, 230, 230)
WHITE_80 = (229, 233, 240)
WHITE_70 = (216, 222, 233)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Игра и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GALAXY ATTACK!!!")
clock = pygame.time.Clock()

# Загрузка всей игровой графики
main = os.path.dirname(__file__)
img_folder = os.path.join(main, "img")
snd_folder = os.path.join(main, "snd")

background = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, "starfield2.jpg")).convert(), (WIDTH, HEIGHT))
background_rect = background.get_rect()
enemy_img = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, "enemyGreen1.png")).convert(), (50,40))
player_img = pygame.image.load(os.path.join(img_folder, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25,19))
player_mini_img.set_colorkey(BLACK)
accuracy_img = pygame.image.load(os.path.join(img_folder, "accuracy.png")).convert()
accuracy_img.set_colorkey(BLACK)

weapons = {
    "bullet": pygame.transform.scale(pygame.image.load(os.path.join(img_folder, "laserRed07.png")).convert(), (13, 35)),
    "laser": pygame.transform.scale(pygame.image.load(os.path.join(img_folder, "laserRed.jpg")).convert(), (11,10))
}
enemy_bullet = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, "laserGreen13.png")).convert(), (13, 35))

meteor_images = []
meteor_images_list =['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
for img in meteor_images_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

explosion_animation = {
    "large": [],
    "small": [],
    "player": []
}
for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pygame.transform.scale(img, (75, 75))
    explosion_animation['large'].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    explosion_animation['small'].append(img_small)
    filename = f"sonicExplosion0{i}.png"
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_animation["player"].append(img)

powerup_images = {
    "shield": pygame.image.load(os.path.join(img_folder, "shield_silver.png")).convert(),
    "weapon": pygame.image.load(os.path.join(img_folder, "bold_silver.png")).convert()
}

# Загрузка мелодий игры 
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "pew.wav"))
expl_sounds = []
for expl in ("expl1.wav", "expl2.wav"):
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder, expl)))
for snd in expl_sounds:
    snd.set_volume(0.1)
pygame.mixer.music.load(os.path.join(snd_folder, "tgfcoder-FrozenJam-SeamlessLoop.mp3"))


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        self.hidden = False
        self.super = False
        self.super_timer = pygame.time.get_ticks()
        self.hide_timer = pygame.time.get_ticks()
        self.shield = 100
        self.image = pygame.transform.scale(player_img, (50, 40)) 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT-25
        self.speedx = 0
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, "bullet")
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.set_volume(0.1)
        shoot_sound.play()
         
    
    def super_shoot(self):
        bullet = Bullet(self.rect.centerx+1, self.rect.top-2, "laser")
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.set_volume(0.06)
        shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, -200)


    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -8
        if keys[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        now = pygame.time.get_ticks()
        if  self.hidden and now - self.hide_timer >= 1000:
            self.hidden = False
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT-25
        if self.super and not (now - self.super_timer >= 1500):
            self.super_shoot()
        else:
            self.super = False
        
# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.speedx = 0
        self.rect.y = -60
        self.speedy = 3
        self.shoot_delay = 300
        self.last_shoot = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot >= self.shoot_delay:
            self.last_shoot = now
            ebullet = enemyBullet(self.rect.centerx, self.rect.bottom)
            enemy_bullets.add(ebullet)
            all_sprites.add(ebullet)
            shoot_sound.set_volume(0.09)
            shoot_sound.play()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top >= 25:
            self.shoot()
            self.speedy = 0
            if self.rect.right >= WIDTH:
                self.speedx = -3
            if self.rect.left <= 0:
                self.speedx = 3
            
# Класс моба
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteor_images)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85//2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -100)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(3, 9)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot += self.rot_speed % 360
            image_copy = pygame.transform.rotate(self.image_original, self.rot)
            mob_center = self.rect.center
            self.image = image_copy
            self.rect = self.image.get_rect()
            self.rect.center = mob_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 40 or self.rect.left < (-20-self.rect.width) or self.rect.right > (WIDTH + 20 + self.rect.width):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-200, -100)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(3, 9)

# Класс снарядов игрока
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = weapons[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # Убить, если  пуля заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

# Класс снарядов врага
class enemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 10
        
    def update(self):
        self.rect.y += self.speedy
        # Убить, если  пуля заходит за нижнюю часть экрана
        if self.rect.bottom > HEIGHT:
            self.kill()

# Класс анимации взрывов
class Explosion(pygame.sprite.Sprite):
    FRAME_RATE = 50

    def __init__(self, center, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = explosion_animation[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > Explosion.FRAME_RATE:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Класс усилений
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "weapon"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
        
    def update(self):
        self.rect.y += self.speedy
        # Убить, если заходит за нижнюю часть экрана
        if self.rect.bottom > HEIGHT:
            self.kill()

# Фон
class Background (pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = background
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, -y + HEIGHT / 2)
        self.y = y
        self.speedy = 6
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y >= -self.y + HEIGHT:
            self.rect.y = -self.y

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Текст
font_name = pygame.font.match_font("ObelixPro")
def draw_text(surf, text, color, size, x, y):
    font = pygame.font.Font(font_name, size)
    surface_font = font.render(text, True, color)
    surface_font_rect = surface_font.get_rect()
    surface_font_rect.midtop = (x,y)
    surf.blit(surface_font, surface_font_rect)

# Здоровье
def draw_shield_bar(surf, x, y, life_points):
    if life_points < 0:
        life_points = 0
    BAR_WIDTH = 100;
    BAR_HEIGHT = 10;
    fill_width = (life_points/100)*BAR_WIDTH 
    fill_rect = pygame.Rect(x, y, fill_width, BAR_HEIGHT)
    border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    pygame.draw.rect(surf, WHITE_100, border_rect)
    pygame.draw.rect(surf, RED, fill_rect) 

# Кол-во жизней
def draw_lives(surf, x, y, lives, img): 
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

# Точность игрока
def draw_accuracy(surf, x, y, img): 
    img_rect = img.get_rect()
    img_rect.x = x
    img_rect.y = y
    surf.blit(img, img_rect)

# Экран-меню
def show_menu_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GALAXY ATTACK", WHITE_70, 40, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Keys \"A\" and \"D\" for movement, space to fire", WHITE_70, 16, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Collect special bonus for super", WHITE_70, 16, WIDTH/2, HEIGHT/2 + 40)
    draw_text(screen, "Press \"ENTER\" to start", WHITE_70, 22, WIDTH/2, HEIGHT*0.75)
    pygame.display.flip()
    waiting = True
    while waiting:
        menu_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    waiting = False
    return menu_time

# Вывод статистики после проигрыша
def show_statistics(time):
    screen.blit(background, background_rect)
    draw_text(screen, "STATISTICS", WHITE_80, 54, WIDTH/2, 80)
    draw_text(screen, f"Score:  {score}", WHITE_80, 20, 107, HEIGHT/4.5 + 100)
    draw_text(screen, f"Accuracy:  {accuracy}%", WHITE_80, 20, 140, HEIGHT/4.5 + 150)
    time = "%.2f" % (time / 1000)
    draw_text(screen, f"Time:  {time} s", WHITE_80, 20, 115.5, HEIGHT/4.5 + 200)
    draw_text(screen, "Press \"ENTER\" to continue", WHITE_80, 20, WIDTH/2, HEIGHT * 0.75)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    waiting = False


enemy_alive = False
# Цикл игры
MENU = True
GAME = True
pygame.mixer.music.play(loops=-1)
while GAME:
    clock.tick(FPS)
    pygame.mixer.music.set_volume(0.1)
    if MENU:
        pygame.mixer.music.set_volume(0.02)
        MENU = False
        menu_time = show_menu_screen()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bg1 = Background(0)
        bg2 = Background(HEIGHT)
        all_sprites.add(bg1)
        all_sprites.add(bg2)
        player = Player()
        all_sprites.add(player)
        for _ in range(2):
            new_mob()
        score = 0
        lucky_hits = 0 
        number_of_shots = 0 
        accuracy = 0
    
# Подсчет продолжительности игры
    game_time = pygame.time.get_ticks() - menu_time


    if player.lives == 0 and not death_explosion.alive():
        pygame.mixer.music.set_volume(0.02)
        show_statistics(game_time)
        MENU = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                number_of_shots += 1

# Начало игры - 2 моба
# 500 очков   - 4 моба
# 1000 очков  - 6 мобов
# 2000 очков  - 8 мобов
# 5000 очков  - 10 мобов
# 7500 очков  - 12 мобов
# 10000 очков - 14 мобов
# 15000 очков - 16 мобов
# 20000 очков - 18 мобов


# Повышение сложности в зависимости от колво очков
    if len(score_list) != 0:
        level = score_list[0]
        if score >= level:
            if level == 5000 or level == 7500 or level == 10000 or level == 15000 or level == 20000:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemy_alive = True
            for _ in range(2):
                new_mob()
            bg1.speedy += 2
            bg2.speedy += 2
            score_list.pop(0)

# Повышение сложности в зависимости от времени
    # if 10000 <= pygame.time.get_ticks() - menu_time <= 10016:
    #     for _ in range(2):
    #         new_mob()
    #     bg1.speedy = 8
    #     bg2.speedy = 8
    # elif 20000 <= pygame.time.get_ticks() - menu_time <= 20016:
    #     for _ in range(2):
    #         new_mob()
    #     bg1.speedy = 10
    #     bg2.speedy = 10
    # elif 30000 <= pygame.time.get_ticks() - menu_time <= 30016:
    #     for _ in range(2):
    #         new_mob()
    #     bg1.speedy = 12
    #     bg2.speedy = 12
    # elif 40000 <= pygame.time.get_ticks() - menu_time <= 40016:
    #     for _ in range(2):
    #         new_mob()
    #     bg1.speedy = 14
    #     bg2.speedy = 14
    # elif 70000 <= pygame.time.get_ticks() - menu_time <= 70016:
    #     for _ in range(4):
    #         new_mob()
    #     bg1.speedy = 16
    #     bg2.speedy = 16
    # elif 100000 <= pygame.time.get_ticks() - menu_time <= 100016:
    #     for _ in range(2):
    #         new_mob()
    #     bg1.speedy = 18
    #     bg2.speedy = 18
    # elif 120000 <= pygame.time.get_ticks() - menu_time <= 120016:
    #     for _ in range(6):
    #         new_mob()
    #     bg1.speedy = 20
    #     bg2.speedy = 20

# Проверка, не ударил ли моб игрока
    hits_with_player = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits_with_player:
        player.shield -= hit.radius*3
        small_expl = Explosion(hit.rect.center, "small")
        all_sprites.add(small_expl)
        new_mob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, "player")
            all_sprites.add(death_explosion)
            player.lives -= 1
            player.shield = 100
            player.hide()
        
# Проверка столкновений пуль и мобов
    hits_with_bullets = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits_with_bullets:
        score += 50 - hit.radius
        if hits_with_bullets[hit][0].type == "bullet":
            lucky_hits += 1
        random.choice(expl_sounds).play()
        large_expl = Explosion(hit.rect.center, "large")
        all_sprites.add(large_expl)
        new_mob()
        if random.randint(0,100) > 97:
             pow = PowerUp(hit.rect.center)
             all_sprites.add(pow)
             powerups.add(pow)
             
# Проверка столкновений игрока и усилений
    hits_with_powerups = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits_with_powerups:
        if hit.type == "shield":
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "weapon":
            player.super = True
            player.super_timer = pygame.time.get_ticks()

# Проверка столкновений игрока и вражеских снарядов
    hits_with_enemybullets = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits_with_enemybullets:
        player.shield -= 45
        small_expl = Explosion(hit.rect.center, "small")
        all_sprites.add(small_expl)
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, "player")
            all_sprites.add(death_explosion)
            player.lives -= 1
            player.shield = 100
            player.hide()

# Проверка столкновений врага и снарядов игрока
    if enemy_alive:
        enemy_and_bullets = pygame.sprite.spritecollide(enemy, bullets, True)
        for hit in enemy_and_bullets:
            enemy.kill()
            enemy_alive = False
            death_explosion = Explosion(enemy.rect.center, "player")
            all_sprites.add(death_explosion)

# Подсчет точности игрока
    if number_of_shots != 0:
        accuracy = "%.2f" % (lucky_hits / number_of_shots * 100)

# Обновление спрайтов
    all_sprites.update()
# Рендеринг
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), WHITE_90, 20, WIDTH//2, 10)
    draw_text(screen, str(accuracy)+"%", WHITE_90, 14, 65, 23)
    draw_accuracy(screen, 5, 20, accuracy_img)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)
# Обновление дисплея
    pygame.display.flip()

pygame.quit()


