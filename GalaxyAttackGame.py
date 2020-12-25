'''Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3'''
import pygame
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE_100 = (255, 255, 255)
WHITE_90 = (230, 230, 230)
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

background = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, "black.png")).convert(), (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25,19))
player_mini_img.set_colorkey(BLACK)

weapons = {
    "bullet": pygame.image.load(os.path.join(img_folder, "laserRed07.png")).convert(),
    "laser": pygame.transform.scale(pygame.image.load(os.path.join(img_folder, "laserRed.jpg")).convert(), (11,10))
}

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
        shoot_sound.play()
    
    def super_shoot(self):
        bullet = Bullet(self.rect.centerx+1, self.rect.top-2, "laser")
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, -200)


    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if self.super and keys[pygame.K_k]:
            self.super_shoot()
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
        if self.super and now - self.super_timer >= 1500:
            self.super = False
        

# Класс моба
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85//2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -60)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(1, 9)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < (0-self.rect.width) or self.rect.right > (WIDTH + self.rect.width):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -60)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(1, 9)

# Класс пули
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
        
    def update(self):
        self.rect.y += 4
        if self.rect.y >= HEIGHT*2:
            self.rect.center = (WIDTH / 2, -self.y + HEIGHT / 2)

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Текст
font_name = pygame.font.match_font("ObelixPro")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    surface_font = font.render(text, True, WHITE_90)
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

# Экран-меню
def show_menu_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GALAXY ATTACK!!!", 40, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Keys \"A\" and \"D\" for movement", 20, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Space to fire , \"K\" for super", 20, WIDTH/2, HEIGHT/2 + 40)
    draw_text(screen, "Press any key to start", 22, WIDTH/2, HEIGHT*0.75)
    pygame.display.flip()
    waiting = True
    while waiting:
        menu_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
    return menu_time

# Цикл игры
MENU = True
GAME = True
pygame.mixer.music.play(loops=-1)
while GAME:
    if MENU:
        pygame.mixer.music.set_volume(0.2)
        MENU = False
        menu_time = show_menu_screen()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        all_sprites.add(Background(0))
        all_sprites.add(Background(HEIGHT))
        player = Player()
        all_sprites.add(player)
        for _ in range(2):
            new_mob()
        score = 0
        
    pygame.mixer.music.set_volume(1)
    clock.tick(FPS)
    if player.lives == 0 and not death_explosion.alive():
        MENU = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    if 10000 <= pygame.time.get_ticks() - menu_time <= 10016:
        for _ in range(2):
            new_mob()
    if 20000 <= pygame.time.get_ticks() - menu_time <= 20016:
       for _ in range(2):
            new_mob()
    if 30000 <= pygame.time.get_ticks() - menu_time <= 30016:
        for _ in range(2):
            new_mob()
    if 40000 <= pygame.time.get_ticks() - menu_time <= 40016:
        for _ in range(2):
            new_mob()
    if 70000 <= pygame.time.get_ticks() - menu_time <= 70016:
        for _ in range(4):
            new_mob()
    if 100000 <= pygame.time.get_ticks() - menu_time <= 100016:
        for _ in range(2):
            new_mob()
    if 120000 <= pygame.time.get_ticks() - menu_time <= 120016:
        for _ in range(6):
            new_mob()


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
        random.choice(expl_sounds).play()
        large_expl = Explosion(hit.rect.center, "large")
        all_sprites.add(large_expl)
        new_mob()
        if random.randint(0,100) > 97:
             pow = PowerUp(hit.rect.center)
             all_sprites.add(pow)
             powerups.add(pow)
             
    # Проверка столкновений игрок и усилений
    hits_with_powerups = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits_with_powerups:
        if hit.type == "shield":
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "weapon":
            player.super = True
            player.super_timer = pygame.time.get_ticks()

    # Обновление спрайтов
    all_sprites.update()
    # Рендеринг
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 19, WIDTH//2, 20)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)

    # Обновление дисплея
    pygame.display.flip()

pygame.quit()


