import pygame
from pygame.locals import *


pygame.init()

clock = pygame.time.Clock()
fps = 60

width, height = 660, 660
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Magical Explore')

# фон
sky_image = pygame.image.load('img/8Sky.png')
hills_image = pygame.image.load('img/7Hills.png')
forest_image = pygame.image.load('img/6Forest.png')
bushes_image = pygame.image.load('img/5BackBushes.png')
ground_image = pygame.image.load('img/4Ground.png')
restart_image = pygame.image.load('img/restart.png')
start_image = pygame.image.load('img/start.png')
exit_image = pygame.image.load('img/exit.png')
menu_image = pygame.image.load('img/menu.png')

tile_size = 55
game_over = 0
main_menu = True


# рисуем клеточное поле
def draw_board():
    for a in range(0, 12):
        pygame.draw.line(screen, (255, 255, 255), (0, a * tile_size), (width, a * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (a * tile_size, 0), (a * tile_size, height))


world_data = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 3, 3, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    #рисуем кнопку
    def draw(self):
        action = False
        position = pygame.mouse.get_pos()
        #кнопка нажата
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
        #движение героя
        dx = 0
        dy = 0
        walk = 2
        if game_over == 0:
            #нажатие на кнопки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 10

            if key[pygame.K_RIGHT]:
                dx += 10

            if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jump is False and self.free is False:
                self.vel_y = -16
                self.jump = True

            if key[pygame.K_SPACE] is False or key[pygame.K_UP] is False:
                self.jump = False
            #анимация
            self.k += 1
            if self.k > walk:
                self.k = 0
                self.ind += 1
                if self.ind >= len(self.images):
                    self.ind = 0
                self.img = self.images[self.ind]

            #гравитация при прыжке
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
             #столкновение
            self.free = True
            for tile in world.tile_list:
                # по x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # по y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #прыжок
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #падение
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.free = False
            #cолкновение с врагами
            if pygame.sprite.spritecollide(self, hedg_group, False):
                game_over = 1
            if pygame.sprite.spritecollide(self, bushes_group, False):
                game_over = 1
                #print(game_over)

            #новые координаты
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > height:
                self.rect.bottom = height
                dy = 0

        #рисуем персонажа на экран
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
        self.move_dir = 1
        self.move_k = 0


player = Player(65, height - 130)
bushes_group = pygame.sprite.Group()
hedg_group = pygame.sprite.Group()
world = World(world_data)

#кнопки
start_button = Button(width // 2 - 320, height // 2 + 125, start_image)
exit_button = Button(width // 2 + 110, height // 2 + 125, exit_image)
restart_button = Button(width // 2 - 100, height // 2 + 150, restart_image)


run = True
while run:
    clock.tick(fps)
    screen.blit(menu_image, (0, 0))
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
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

        if game_over == 0:
            hedg_group.update()

        hedg_group.draw(screen)
        bushes_group.draw(screen)

        game_over = player.update(game_over)
        #когда прсонаж умирает
        if game_over == 1:
            if restart_button.draw():
                player.reset(65, height - 130)
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()

pygame.quit()
