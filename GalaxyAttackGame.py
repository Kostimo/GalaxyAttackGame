'''Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3'''
import pygame
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Игра и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("!!!GALAXY ATTACK!!!")
clock = pygame.time.Clock()

# Загрузка всей игровой графики
main = os.path.dirname(__file__)
img_folder = os.path.join(main, "img")
snd_folder = os.path.join(main, "snd")

background = pygame.image.load(os.path.join(img_folder, "starfield.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_folder, "laserRed07.png")).convert()

meteor_images = []
meteor_images_list =['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
for img in meteor_images_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "pew.wav"))
expl_sounds = []
for expl in ("expl1.wav", "expl2.wav"):
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder, expl)))
pygame.mixer.music.load(os.path.join(snd_folder, "tgfcoder-FrozenJam-SeamlessLoop.mp3"))
# pygame.mixer.music.set_volume(0.7)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

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
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -60)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(1, 8)

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
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

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

for _ in range(8):
    new_mob()

score = 0

# Рендеринг очков
font_name = pygame.font.match_font("ObelixPro")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    surface_font = font.render(text, True, WHITE)
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
    pygame.draw.rect(surf, WHITE, border_rect)
    pygame.draw.rect(surf, RED, fill_rect) 

pygame.mixer.music.play(loops=-1)
# Цикл игры
GAME = True
while GAME:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Проверка, не ударил ли моб игрока
    hits_with_player = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits_with_player:
        player.shield -= hit.radius*2
        new_mob()
        if player.shield <= 0:
            GAME = False
        

    # Проверка столкновений пуль и мобов
    hits_with_bullets = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits_with_bullets:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        new_mob()

    # Обновление спрайтов
    all_sprites.update()

    # Рендеринг
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 19, WIDTH//2, 20)
    draw_shield_bar(screen, 5, 5, player.shield)

    # Обновление дисплея
    pygame.display.flip()

pygame.quit()


