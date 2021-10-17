import pygame
import os
import csv

pygame.init()

# frame rate
clock = pygame.time.Clock()
fps = 60

screen_width = 1024
screen_height = 576

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PWS")

tile_size = 64
tile_types = 2
cols = 48
rows = 27
game_over = False
level = 0
current_world = 0
world_types = 1
game_started = False

gravity = 0.75

moving_left = False
moving_right = False
shoot = False

scroll_threshold_hor = 4 * tile_size
scroll_threshold_ver = tile_size
scroll_hor = 0
scroll_ver = 0
scroll_speed = 1
total_hor_scroll = 0
total_ver_scroll = 0

# images
start_img = pygame.image.load("img/New Piskel.png")
exit_img = pygame.image.load("img/New Piskel.png")
respawn_img = pygame.image.load("img/New Piskel.png")

# background images
bg_img_list = []
for x in range(world_types):
    img = pygame.image.load(f"img/World/{x}.png")
    img = pygame.transform.scale(img, (screen_width, screen_height))
    bg_img_list.append(img)

# tile images
tile_img_list = []
for x in range(tile_types):
    img = pygame.image.load(f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    tile_img_list.append(img)
# projectile images
arrow_img = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (10, 10))
# item images
health_img = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (10, 10))
mana_img = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (10, 10))
item_dict = {
    "Health": health_img,
    "Mana": mana_img
}

# font
font = pygame.font.SysFont("Futura", 30)


def draw_bg():
    # screen.blit(bg_img_list[current_world], (0,0))
    screen.fill((150, 200, 50))


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def reset_level():
    arrow_group.empty()
    item_group.empty()
    decoration_group.empty()
    lava_group.empty()
    data = []
    for row in range(rows):
        r = [-1] * cols
        data.append(r)
    return data


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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 10
        self.max_health = 15
        self.speed = speed
        self.shoot_cooldown = 0
        self.direction = 1
        self.jump = False
        self.in_air = True
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load in images for player
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/Player/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/Player/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (tile_size, tile_size))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        scroll_hor = 0
        scroll_ver = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump and not self.in_air:
            self.vel_y = -20
            self.jump = False
            self.in_air = True

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = scroll_ver
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
            dx = 0

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        if (self.rect.right > screen_width - scroll_threshold_hor and
            total_hor_scroll < (world.level_length * tile_size) - screen_width) \
                or (self.rect.left < scroll_threshold_hor and total_hor_scroll > abs(dx)):
            self.rect.x -= int(dx)
            scroll_hor = -dx

        if self.rect.top < scroll_threshold_ver and not total_ver_scroll <= scroll_threshold_ver:
            self.rect.top = scroll_threshold_ver
            scroll_ver -= self.vel_y
        if self.rect.bottom > screen_height - scroll_threshold_ver and \
                total_ver_scroll < (world.level_height * tile_size) - screen_height:
            self.rect.y -= int(dy)
            scroll_ver = -self.vel_y

        return scroll_hor, scroll_ver

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.index = len(self.animation_list[self.action]) - 1
            else:
                self.index = 0

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            arrow = Arrow(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                          self.direction)
            arrow_group.add(arrow)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        self.level_height = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    image = tile_img_list[tile]
                    img_rect = image.get_rect()
                    img_rect.x = x * tile_size
                    img_rect.y = y * tile_size
                    tile_data = (image, img_rect)
                    if tile == 0:
                        self.obstacle_list.append(tile_data)
                    elif tile == 1:
                        player = Player(x * tile_size, y * tile_size, 5)
                    elif 11 <= tile <= 13:
                        lava = Lava(image, x * tile_size, y * tile_size)
                        lava_group.add(lava)
                    elif 13 <= tile <= 15:
                        decoration = Decoration(img, x * tile_size, y * tile_size)
                        decoration_group.add(decoration)
                    elif tile == 16:
                        item = Item(x * tile_size, y * tile_size, "Health")
                        item_group.add(item)
                    elif tile == 20:
                        pass
        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += int(scroll_hor)
            tile[1][1] += int(scroll_ver)
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += scroll_hor
        self.rect.y += scroll_ver


class Lava(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += scroll_hor
        self.rect.y += scroll_ver


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_dict[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + tile_size - self.image.get_height())

    def update(self):
        self.rect.x += scroll_hor
        self.rect.y += scroll_ver
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Mana":
                pass
            self.kill()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = arrow_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()


# sprite groups
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

start_btn = Button(screen_width//2 - 130, screen_height // 2 - 150, start_img)
exit_btn = Button(screen_width//2 - 130, screen_height // 2 + 50, exit_img)
respawn_btn = Button(screen_width//2 - 130, screen_height // 2 - 150, respawn_img)


world_data = []
for row in range(rows):
    r = [-1] * cols
    world_data.append(r)

with open(f"level_data/level_data{level}.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player = world.process_data(world_data)

run = True
while run:
    if game_started:
        draw_bg()
        world.draw()
        for x in range(player.max_health):
            screen.blit(health_img, (90 + (x * 20), 40))
        for x in range(player.health):
            screen.blit(health_img, (90 + (x * 20), 40))

        player.update()
        player.draw()

        # update + draw groups
        arrow_group.update()
        item_group.update()
        decoration_group.update()
        lava_group.update()
        arrow_group.draw(screen)
        item_group.draw(screen)
        decoration_group.draw(screen)
        lava_group.draw(screen)

        if player.alive:
            if shoot:
                player.shoot()
                player.update_action(3)
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)

            scroll_hor, scroll_ver = player.move(moving_left, moving_right)
            total_hor_scroll -= scroll_hor
            total_ver_scroll -= scroll_ver
        else:
            scroll_ver = 0
            scroll_hor = 0
            if respawn_btn():
                total_hor_scroll = 0
                total_ver_scroll = 0
                world_data = reset_level()
                with open(f"level_data/level_data{level}.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                world = World()
                player = world.process_data(world_data)

    else:
        screen.fill((100, 100, 200))
        if start_btn.draw():
            game_started = True
        if exit_btn.draw():
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.K_ESCAPE:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    clock.tick(fps)
    pygame.display.update()

pygame.quit()
