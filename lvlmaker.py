import pygame
import csv

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1024
screen_height = 576
lower_margin = 100
side_margin = 300

rows = 27
cols = 48
level = 0
tile_size = 64
tiles_types = 1
current_tile = 0

scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_hor = 0
scroll_ver = 0
scroll_speed = 1

# load images
img_list = []
for x in range(tiles_types):
    img = pygame.image.load(f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

save_img = pygame.image.load(f"img/New Piskel.png")
load_img = pygame.image.load(f"img/New Piskel.png")
screen = pygame.display.set_mode((side_margin + screen_width, lower_margin + screen_height))
pygame.display.set_caption("level editor")

world_data = []
for row in range(rows):
    r = [-1] * cols
    world_data.append(r)

for tile in range(cols):
    world_data[rows - 1][tile] = 0
print(world_data)

font = pygame.font.SysFont("Futura", 30)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill((0, 0, 0))
    image = pygame.transform.scale(pygame.image.load("img/dirt.png"), (screen_width, screen_height))
    width = screen_width
    height = screen_height
    for x in range(3):
        for y in range(3):
            screen.blit(image, ((x * width) - scroll_hor, (y * height) - scroll_ver))


def draw_grid():
    for c in range(cols + 1):
        pygame.draw.line(screen, (255, 255, 255), (c * tile_size - scroll_hor, 0),
                         (c * tile_size - scroll_hor, 4 * screen_height))
    for c in range(rows + 1):
        pygame.draw.line(screen, (255, 255, 255), (0, c * tile_size - scroll_ver),
                         (4 * screen_width, c * tile_size - scroll_ver))


def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * tile_size - scroll_hor, y * tile_size - scroll_ver))


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

save_button = Button(screen_width // 2, screen_height + lower_margin - 50, save_img)
load_button = Button(screen_width // 2 + 200, screen_height + lower_margin - 50, load_img)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(screen_width + (75 + button_col) + 50, 75 * button_row + 50, img_list[i])
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True
while run:
    clock.tick(fps)
    draw_bg()
    draw_world()
    draw_grid()

    pygame.draw.rect(screen, (100, 200, 100), (screen_width, 0, side_margin, screen_height))
    pygame.draw.rect(screen, (100, 200, 100), (0, screen_height, screen_width + side_margin, lower_margin))
    draw_text(f"level: {level}", font, (255, 255, 255), 10, screen_height + lower_margin - 90)
    draw_text("W or S to chance level", font, (255, 255, 255), 10, screen_height + lower_margin - 50)
    save_button.draw()
    load_button.draw()

    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw():
            current_tile = button_count

    pygame.draw.rect(screen, (255, 255, 255), button_list[current_tile].rect, 1)

    if scroll_left and scroll_hor > 0:
        scroll_hor -= 5 * scroll_speed
    elif scroll_right and scroll_hor < (cols * tile_size) - screen_width:
        scroll_hor += 5 * scroll_speed
    elif scroll_down and scroll_ver < (rows * tile_size) - screen_height:
        scroll_ver += 5 * scroll_speed
    elif scroll_up and scroll_ver > 0:
        scroll_ver -= 5 * scroll_speed

    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll_hor) // tile_size
    y = (pos[1] + scroll_ver) // tile_size
    if pos[0] < screen_width and pos[1] < screen_height:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

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
            if event.key == pygame.K_w:
                level += 1
            if event.key == pygame.K_s and level > 0:
                level -= 1
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
