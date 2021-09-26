import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1024
screen_height = 576
lower_margin = 100
side_margin = 300

rows = 27
cols = 48
tile_size = 64

scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_hor = 0
scroll_ver = 0
scroll_speed = 1

screen = pygame.display.set_mode((side_margin + screen_width, lower_margin + screen_height))
pygame.display.set_caption("level editor")

def draw_bg():
    screen.fill((0, 0, 0))
    img = pygame.transform.scale(pygame.image.load("img/dirt.png"), (screen_width, screen_height))
    width = screen_width
    height = screen_height
    for x in range(3):
        for y in range(3):
            screen.blit(img,((x * width) - scroll_hor, (y * height) - scroll_ver))

def draw_grid():
    for c in range(cols + 1):
        pygame.draw.line(screen, (255,255,255), (c * tile_size - scroll_hor, 0), (c * tile_size - scroll_hor, 4 * screen_height))
    for c in range(rows + 1):
        pygame.draw.line(screen, (255,255,255), (0, c * tile_size - scroll_ver), (4 * screen_width, c * tile_size - scroll_ver))

run = True
while run:
    clock.tick(fps)
    draw_bg()
    draw_grid()

    if scroll_left and scroll_hor > 0:
        scroll_hor -= 5 * scroll_speed
    elif scroll_right:
        scroll_hor += 5 * scroll_speed
    elif scroll_down:
        scroll_ver += 5 * scroll_speed
    elif scroll_up:
        scroll_ver -= 5 * scroll_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1


    pygame.display.update()

pygame.quit()