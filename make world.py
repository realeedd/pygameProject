import pygame

pygame.init()

size = 630, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Magical Explore')

bg_image = pygame.image.load('img/forest.png')

run = True

while run:
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
