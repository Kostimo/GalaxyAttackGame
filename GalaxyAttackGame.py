import pygame

WIDTH = 400
HEIGHT = 600
FPS = 24

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,  HEIGHT//2)
    def update(self):
        self.rect.x += 7
        if self.rect.x > WIDTH:
            self.rect.right = 0

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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
    screen.fill((0, 255, 255))
    all_sprites.draw(screen)
    #обновление дисплея
    pygame.display.update()


