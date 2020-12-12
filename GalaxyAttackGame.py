import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT-25
        self.speedx = 0

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

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(1, 8)

all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(8):
    m = Mob()
    all_sprites.add(m)

#игра и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOTER!")
clock = pygame.time.Clock()

#цикл игры
GAME = True
while GAME:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False

    #обновление спрайтов
    all_sprites.update()

    #рендеринг
    screen.fill((BLACK))
    all_sprites.draw(screen)

    #обновление дисплея
    pygame.display.flip()

pygame.quit()


