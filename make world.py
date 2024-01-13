import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

width, height = 650, 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Magical Explore')

# фон
sky_image = pygame.image.load('img/8Sky.png')
hills_image = pygame.image.load('img/7Hills.png')
forest_image = pygame.image.load('img/6Forest.png')
bushes_image = pygame.image.load('img/5BackBushes.png')
ground_image = pygame.image.load('img/4Ground.png')

tile_size = 65


# рисуем клеточное поле
def draw_board():
    for a in range(0, 10):
        pygame.draw.line(screen, (255, 255, 255), (0, a * tile_size), (width, a * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (a * tile_size, 0), (a * tile_size, height))


world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


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
                c_k += 1
            r_k += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Player():
    def __init__(self, x, y):
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

    def update(self):
        # движение героя
        dx = 0
        dy = 0
        walk = 2
        # нажатие на кнопки
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 10

        if key[pygame.K_RIGHT]:
            dx += 10

        if key[pygame.K_SPACE] and self.jump is False:
            self.vel_y = -15
            self.jump = True

        if key[pygame.K_SPACE] is False:
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

        # новые координаты
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0

        # рисуем персонажа на экран
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)




world = World(world_data)
player = Player(65, height - 130)

run = True
while run:
    clock.tick(fps)
    # загружаем фон
    screen.blit(sky_image, (0, 0))
    screen.blit(hills_image, (0, 0))
    screen.blit(forest_image, (0, 0))
    screen.blit(bushes_image, (0, 0))
    screen.blit(ground_image, (0, 0))
    # рисуем поле
    draw_board()
    world.draw()
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
