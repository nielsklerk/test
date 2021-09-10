import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 500
tile_size = 50

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PWS")

run = True
while run:

    pygame.display.update()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
