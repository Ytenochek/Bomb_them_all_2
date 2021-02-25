import os
import sys
import random
import pygame


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bomb them all 2")

all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.exploded = False
        self.set_rect()

    def set_rect(self):
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(height - self.rect.height)

    def update(self, *args):
        if (
            args
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(args[0].pos)
            and not self.exploded
        ):
            self.image = self.image_boom
            self.rect = self.image.get_rect()
            self.rect.center = args[0].pos
            self.exploded = True


for _ in range(20):
    bomb = Bomb(all_sprites)
    col = pygame.sprite.spritecollideany(bomb, all_sprites)
    while bomb != col:
        bomb.set_rect()
        col = pygame.sprite.spritecollideany(bomb, all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    all_sprites.update(event)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
