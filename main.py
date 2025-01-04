import os.path
import random

import pygame

pygame.init()
_size = _width, _height = 1000, 800  # 500x500 слишком мало для 20 бомбочек
_main_screen = pygame.display.set_mode(_size)
_main_sprite_group = pygame.sprite.Group()
_bomb_sprite_group = pygame.sprite.Group()


def load_image(filename: str | os.PathLike, colorkey=None) -> pygame.Surface:
    fullname = os.path.join('data', filename)
    if not os.path.isfile(fullname):
        pass
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    bomb_image = load_image('bomb.png')
    boom_image = load_image('boom.png')

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Bomb.bomb_image
        self.rect = self.image.get_rect()
        attempts = 0
        self.rect.x = random.randint(self.rect.width, _width - self.rect.width)
        self.rect.y = random.randint(self.rect.height, _height - self.rect.height)
        while pygame.sprite.spritecollideany(self, _bomb_sprite_group):
            attempts += 1
            self.rect.x = random.randint(self.rect.width, _width - self.rect.width)
            self.rect.y = random.randint(self.rect.height, _height - self.rect.height)
            if attempts > 100:
                _bomb_sprite_group.clear(_main_screen, _main_screen)
        _bomb_sprite_group.add(self)

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = Bomb.boom_image


class MainWindow:
    def __init__(self):
        self.fps = 60
        self.size = _size
        self.screen = _main_screen
        self.main_sprite_group = _main_sprite_group
        for _ in range(20):
            Bomb(self.main_sprite_group)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.main_sprite_group.update(event)

            self.main_sprite_group.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    window = MainWindow()
    window.run()
