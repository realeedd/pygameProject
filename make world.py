import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

width, height = 650, 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Magical Explore')

#фон
sky_image = pygame.image.load('img/8Sky.png')
hills_image = pygame.image.load('img/7Hills.png')
forest_image = pygame.image.load('img/6Forest.png')
bushes_image = pygame.image.load('img/5BackBushes.png')
ground_image = pygame.image.load('img/4Ground.png')

tile_size = 65


#рисуем клеточное поле
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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


class Player():
    def __init__(self, x, y):
        img = pygame.image.load('img/Sprite-0001.png')
        self.img = pygame.transform.scale(img, (50, 65))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jump = False

    def update(self):
        #движение героя
        dx = 0
        dy = 0
        #нажатие на кнопки
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

        #гравитация при прыжке
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #новые координаты
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0

        #рисуем персонажа на экран
        screen.blit(self.img, self.rect)



world = World(world_data)
player = Player(65, height - 130)

run = True
while run:
    clock.tick(fps)
    #загружаем фон
    screen.blit(sky_image, (0, 0))
    screen.blit(hills_image, (0, 0))
    screen.blit(forest_image, (0, 0))
    screen.blit(bushes_image, (0, 0))
    screen.blit(ground_image, (0, 0))
    #рисуем поле
    draw_board()
    world.draw()
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
