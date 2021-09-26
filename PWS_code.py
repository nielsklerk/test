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
tile_types = 20
cols = 48
rows = 27
game_over = False

gravity = 0.75

moving_left = False
moving_right = False
shoot = False

# images
# tile images
img_list = []
for x in range(tile_types):
    img = pygame.image.load(f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)
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
    screen.fill((100, 100, 100))
    pygame.draw.line(screen, (255, 0, 0), (0, 500), (screen_width, 500))


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
                img = pygame.transform.scale(img, (50, 100))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        if self.rect.bottom + dy > 500:
            dy = 500 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

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


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tile_size
                    img_rect.y = y * tile_size
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 10:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 11 and tile <= 13:
                        lava = Lava(img, x * tile_size, y * tile_size)
                        lava_group.add(lava)
                    elif tile >= 13 and tile <= 15:
                        decoration = Decoration(img, x * tile_size, y * tile_size)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = Player(x * tile_size, y * tile_size, 5)
                    elif tile == 16:
                        item = Item(x * tile_size, y * tile_size, "Health")
                        item_group.add(item)
                    elif tile == 20:
                        pass
        return player

    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))


class Lava(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_dict[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + tile_size - self.image.get_height())

    def update(self):
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


# sprite groups
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

world_data = []
for row in range(rows):
    r = [-1] * cols
    world_data.append(r)

with open("level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player = world.process_data(world_data)

run = True
while run:

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
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
