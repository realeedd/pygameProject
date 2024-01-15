import pygame
from pygame.locals import *
import pickle

from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60


names = []

width, height = 660, 660
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Wizard')

# музыка
pygame.mixer.music.load('img/Good Day So Far!.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
pygame.mixer.music.set_volume(0.2)

coin_sound = pygame.mixer.Sound('img/coin.wav')
coin_sound.set_volume(0.5)
jump_sound = pygame.mixer.Sound('img/jump.wav')
jump_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('img/game_over.wav')
game_over_sound.set_volume(0.5)

tile_size = 55
game_over = 0
main_menu = True
level = 1
levels_menu = False
# количество монеток
k = 0
# для текста
font = pygame.font.SysFont('Pixel Digivolve Cyrillic', 40)
font_game_over = pygame.font.SysFont('Pixel Digivolve Cyrillic', 70)
white = (255, 255, 255)
red = pygame.Color('red')

# фон
sky_image = pygame.image.load('img/8Sky.png')
hills_image = pygame.image.load('img/7Hills.png')
forest_image = pygame.image.load('img/6Forest.png')
bushes_image = pygame.image.load('img/5BackBushes.png')
ground_image = pygame.image.load('img/4Ground.png')
# кнопки
restart_image = pygame.image.load('img/restart.png')
start_image = pygame.image.load('img/start.png')
exit_image = pygame.image.load('img/exit.png')
menu_image = pygame.image.load('img/menu.png')
levels_image = pygame.image.load('img/levels.png')
go_image = pygame.image.load('img/go.png')

# значки уровней
first_image = pygame.image.load('img/first.png')
second_image = pygame.image.load('img/second.png')
third_image = pygame.image.load('img/third.png')
fourth_image = pygame.image.load('img/fourth.png')
fifth_image = pygame.image.load('img/fifth.png')


# рисуем клеточное поле
def draw_board():
    for a in range(0, 12):
        pygame.draw.line(screen, (255, 255, 255), (0, a * tile_size), (width, a * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (a * tile_size, 0), (a * tile_size, height))


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# загрузка нового уровня
def reset_level(level):
    player.reset(65, height - 130)
    hedg_group.empty()
    bushes_group.empty()
    exit_group.empty()
    coin_group.empty()
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


'''
world_data = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 4, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 3, 3, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
'''


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    # рисуем кнопку
    def draw(self):
        action = False
        position = pygame.mouse.get_pos()
        # кнопка нажата
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 or pygame.key.get_pressed()[K_RETURN] and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        # движение героя
        dx = 0
        dy = 0
        walk = 2
        if game_over == 0:
            # нажатие на кнопки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 10

            if key[pygame.K_RIGHT]:
                dx += 10

            if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jump is False and self.free is False:
                jump_sound.play()
                self.vel_y = -16
                self.jump = True

            if key[pygame.K_SPACE] is False or key[pygame.K_UP] is False:
                self.jump = False
            # анимация
            self.k += 1
            if self.k > walk:
                self.k = 0
                self.ind += 1
                if self.ind >= len(self.images):
                    self.ind = 0
                self.img = self.images[self.ind]

            # гравитация при прыжке
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            # столкновение
            self.free = True
            for tile in world.tile_list:
                # по x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # по y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # прыжок
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # падение
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.free = False
            # cолкновение с врагами
            if pygame.sprite.spritecollide(self, hedg_group, False):
                game_over = 1
                game_over_sound.play()
            if pygame.sprite.spritecollide(self, bushes_group, False):
                game_over = 1
                game_over_sound.play()
                # print(game_over)
            # прохождение уровня
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 2

            # новые координаты
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > height:
                self.rect.bottom = height
                dy = 0
        elif game_over == 1:
            draw_text('Вы погибли', font_game_over, red, (width // 2) - 220, height // 2)
        # рисуем персонажа на экран
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.images = []
        self.ind = 0
        # спрайты персонажа
        self.k = 0
        for n in range(1, 14):
            img = pygame.image.load(f'img/Sprite-{n}.png')
            img = pygame.transform.scale(img, (50, 65))
            self.images.append(img)

        self.img = self.images[self.ind]
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.vel_y = 0
        self.jump = False
        self.free = True


class World():
    def __init__(self, data):
        self.tile_list = []

        grass_image = pygame.image.load('img/grass.png')

        r_k = 0
        for row in data:
            c_k = 0
            for tile in row:
                if tile == 1:
                    background = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    background_rect = background.get_rect()
                    background_rect.x = c_k * tile_size
                    background_rect.y = r_k * tile_size
                    tile = (background, background_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    hedg = Enemy(c_k * tile_size, r_k * tile_size)
                    hedg_group.add(hedg)
                if tile == 3:
                    bush = Bushes(c_k * tile_size, r_k * tile_size)
                    bushes_group.add(bush)
                if tile == 4:
                    exit = Exit(c_k * tile_size, r_k * tile_size - 45)
                    exit_group.add(exit)
                if tile == 5:
                    coin = Coins(c_k * tile_size + 20, r_k * tile_size + 30)
                    coin_group.add(coin)
                c_k += 1
            r_k += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/hedg1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_dir = 1
        self.move_k = 0

    def update(self):
        self.rect.x += self.move_dir
        self.move_k += 1
        if abs(self.move_k) > 50:
            self.move_dir *= -1
            self.move_k = 0


class Bushes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/Bush.png')
        self.image = pygame.transform.scale(img, (65, 58))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/crystal.png')
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit_door.png')
        self.image = pygame.transform.scale(img, (55, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(55, height - 130)

bushes_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
hedg_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

coin_pic = Coins(tile_size // 2, tile_size // 2)
coin_group.add(coin_pic)

# уровни
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

# кнопки
start_button = Button(width // 2 - 320, height // 2 - 100, start_image)
exit_button = Button(width // 2 + 120, height // 2 + 230, exit_image)
levels_button = Button(width // 2 + - 320, height // 2, levels_image)
restart_button = Button(width // 2 - 100, height // 2 + 150, restart_image)
go_button = Button(width // 2 + - 320, height // 2, go_image)


# кнопки выбора уровня
first_button = Button(width // 2 - 300, height // 2 - 100, first_image)
second_button = Button(width // 2 - 100, height // 2 - 100, second_image)
third_button = Button(width // 2 + 150, height // 2 - 100, third_image)
fourth_button = Button(width // 2 - 200, height // 2 + 50, fourth_image)
fifth_button = Button(width // 2 + 70, height // 2 + 50, fifth_image)


def main():
    screen.blit(menu_image, (0, 0))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 200, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        if exit_button.draw():
            pygame.quit()
        if go_button.draw() and len(names) != 0:
            done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                #когда нажали на input()
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # меняет цвет input()
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        names.append(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, white)
        width_text = max(200, txt_surface.get_width()+10)
        input_box.w = width_text
        draw_text('Кликните на окошко снизу,', font, white, (width - 610), (height - 590))
        draw_text('введите свой никнейм и нажмите клавишу ENTER', font, white, (width - 610), (height - 550))
        draw_text('Для продолжения нажмите кнопку GO!', font, white, (width - 580), (height - 400))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()


run = True
while run:
    clock.tick(fps)
    screen.blit(menu_image, (0, 0))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
        if levels_button.draw():
            main_menu = False
            levels_menu = True
    # меню
    elif levels_menu == True:
        screen.blit(menu_image, (0, 0))
        if first_button.draw():
            levels_menu = False
            level = 1
            world_data = []
            world = reset_level(level)
            game_over = 0

        if second_button.draw():
            levels_menu = False
            level = 2
            world_data = []
            world = reset_level(level)
            game_over = 0

        if third_button.draw():
            levels_menu = False
            level = 3
            world_data = []
            world = reset_level(level)
            game_over = 0

        if fourth_button.draw():
            levels_menu = False
            level = 4
            world_data = []
            world = reset_level(level)
            game_over = 0

        if fifth_button.draw():
            levels_menu = False
            level = 5
            world_data = []
            world = reset_level(level)
            game_over = 0

    else:
        # загружаем фон
        screen.blit(sky_image, (0, 0))
        screen.blit(hills_image, (0, 0))
        screen.blit(forest_image, (0, 0))
        screen.blit(bushes_image, (0, 0))
        screen.blit(ground_image, (0, 0))
        # рисуем поле
        draw_board()
        world.draw()

        hedg_group.draw(screen)
        bushes_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        if game_over == 0:
            hedg_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_sound.play()
                k += 1
            draw_text('X ' + str(k), font, white, tile_size, 10)

        game_over = player.update(game_over)
        # когда персонаж умирает
        if game_over == 1:
            if restart_button.draw():
                world_data = []
                player.reset(65, height - 130)
                game_over = 0
                k = 0

        # прохождение уровня
        if game_over == 2:
            level += 1
            if level <= 5:
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('Игра пройдена!', font_game_over, red, (width // 2) - 320, height // 2)
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    k = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

pygame.quit()
