import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
tile_size = 55
cols = 12
margin = 100
screen_width = 660
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

# load images
sky_image = pygame.image.load('img/8Sky.png')
hills_image = pygame.image.load('img/7Hills.png')
forest_image = pygame.image.load('img/6Forest.png')
bushes_image = pygame.image.load('img/5BackBushes.png')
ground_image = pygame.image.load('img/4Ground.png')
grass_image = pygame.image.load('img/grass.png')
hedg_image = pygame.image.load('img/hedg1.png')
bush_image = pygame.image.load('img/Bush.png')

exit_img = pygame.image.load('img/exit_door.png')
save_img = pygame.image.load('img/saveLevel.png')
load_img = pygame.image.load('img/load.png')

# define game variables
clicked = False
level = 1

# define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

# create empty tile list
world_data = []
for row in range(12):
    r = [0] * 12
    world_data.append(r)

# create boundary
for tile in range(0, 12):
    world_data[11][tile] = 1
    world_data[0][tile] = 1
    world_data[tile][0] = 1
    world_data[tile][11] = 1


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_grid():
    for c in range(21):
        # vertical lines
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
        # horizontal lines
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
    for row in range(12):
        for col in range(12):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    # grass blocks
                    img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    # enemy blocks
                    img = pygame.transform.scale(hedg_image, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    # lava
                    img = pygame.transform.scale(bush_image, (65, 58))
                    screen.blit(img, (col * tile_size, row * tile_size))

                if world_data[row][col] == 4:
                    # exit
                    img = pygame.transform.scale(exit_img, (55, 100))
                    screen.blit(img, (col * tile_size, row * tile_size - 45))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# create load and save buttons
save_button = Button(500, 670, save_img)


# main game loop
run = True
while run:

    clock.tick(fps)

    # draw background
    screen.fill(green)
    screen.blit(sky_image, (0, 0))
    screen.blit(hills_image, (0, 0))
    screen.blit(forest_image, (0, 0))
    screen.blit(bushes_image, (0, 0))
    screen.blit(ground_image, (0, 0))

    # show the grid and draw the level tiles
    draw_grid()
    draw_world()

    if save_button.draw():
        # save level data
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()

    # text showing current level
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            # check that the coordinates are within the tile area
            if x < 12 and y < 12:
                # update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 4:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 4
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        # up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1

    # update game display window
    pygame.display.update()

pygame.quit()
