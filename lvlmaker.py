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
tile_types = 34
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
for x in range(tile_types):
    img = pygame.image.load(f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

save_img = pygame.image.load(f"img/Button/Save.png")
save_img = pygame.transform.scale(save_img, (2 * save_img.get_width(), 2 * save_img.get_height()))
load_img = pygame.image.load(f"img/Button/Load.png")
load_img = pygame.transform.scale(load_img, (2 * load_img.get_width(), 2 * load_img.get_height()))
screen = pygame.display.set_mode((side_margin + screen_width, lower_margin + screen_height))
pygame.display.set_caption("level editor")

world_data = []
for row in range(rows):
    r = [-1] * cols
    world_data.append(r)

font = pygame.font.SysFont(pygame.font.get_fonts()[41], 30)


def draw_text(text, fonttype, color, xcoords, ycoords):
    txt_img = fonttype.render(text, True, color)
    screen.blit(txt_img, (xcoords, ycoords))


def draw_bg(world):
    screen.fill((0, 0, 0))
    image = pygame.transform.scale(pygame.image.load(f"img/World/{world}.png"), (screen_width, screen_height))
    width = screen_width
    height = screen_height
    for xcoords in range(3):
        for ycoords in range(3):
            screen.blit(image, ((xcoords * width) - scroll_hor, (ycoords * height) - scroll_ver))


def draw_grid():
    for c in range(cols + 1):
        pygame.draw.line(screen, (255, 255, 255), (c * tile_size - scroll_hor, 0),
                         (c * tile_size - scroll_hor, 4 * screen_height))
    for c in range(rows + 1):
        pygame.draw.line(screen, (255, 255, 255), (0, c * tile_size - scroll_ver),
                         (4 * screen_width, c * tile_size - scroll_ver))


def draw_world():
    for ycoords, one_row in enumerate(world_data):
        for xcoords, one_tile in enumerate(one_row):
            if one_tile >= 0:
                screen.blit(img_list[one_tile], (xcoords * tile_size - scroll_hor, ycoords * tile_size - scroll_ver))


class Button:
    def __init__(self, xcoords, ycoords, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = xcoords
        self.rect.y = ycoords
        self.clicked = False

    def draw(self):
        action = False

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


save_button = Button(screen_width // 2, screen_height + lower_margin - 80, save_img)
load_button = Button(screen_width // 2 + 200, screen_height + lower_margin - 80, load_img)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(screen_width + (30 * button_col) + 5, 30 * button_row + 10, pygame.transform.scale(img_list[i],
                                                                                                            (20, 20)))
    button_list.append(tile_button)
    button_col += 1
    if button_col == 10:
        button_row += 1
        button_col = 0


run = True
while run:
    clock.tick(fps)
    if 0 <= level <= 6:
        draw_bg(0)

    draw_world()
    draw_grid()

    pygame.draw.rect(screen, (100, 100, 100), (screen_width, 0, side_margin, screen_height))
    pygame.draw.rect(screen, (100, 100, 100), (0, screen_height, screen_width + side_margin, lower_margin))
    draw_text(f"level: {level}", font, (255, 255, 255), 10, screen_height + lower_margin - 90)
    draw_text("W or S to chance level", font, (255, 255, 255), 10, screen_height + lower_margin - 50)

    if save_button.draw():
        with open(f"level_data/level_data{level}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in world_data:
                writer.writerow(row)
    if load_button.draw():
        scroll_hor = 0
        scroll_ver = 0
        with open(f"level_data/level_data{level}.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

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
