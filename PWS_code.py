import pygame
from pygame import mixer
import os
import csv

pygame.init()
mixer.init()

# frame rate
clock = pygame.time.Clock()
fps = 60

# screen size
screen_width = 1024
screen_height = 576

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PWS")

tile_size = 64
tile_types = 34
cols = 48
rows = 27
game_over = False
previous_level = "Left"
level = 0
current_world = 15
world_types = 3
game_started = False
hor_offset = 0
ver_offset = 0

gravity = 0.75

# action variables
moving_left = False
moving_right = False
shoot = False
cast = False
walljump_acquired = False
doublejump_acquired = True
emerald_acquired = False
ruby_acquired = False
sapphire_acquired = False
map_menu = False

# scroll variables
scroll_threshold_hor = 4 * tile_size
scroll_threshold_ver = 2 * tile_size
scroll_hor = 0
scroll_ver = 0
scroll_speed = 1
total_hor_scroll = 0
total_ver_scroll = 0
"""
# load music and sounds
pygame.mixer.music.load("audio/sound.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 4000)
jump_fx = pygame.mixer.Sound("audio/jump.wav")
jump_fx.set_volume(0.5)
cast_fx = pygame.mixer.Sound("audio/cast.wav")
cast_fx.set_volume(0.5)
shoot_fx = pygame.mixer.Sound("audio/shoot.wav")
shoot_fx.set_volume(0.5)
"""
# images
# button images
start_img = pygame.image.load("img/New Piskel.png")
exit_img = pygame.image.load("img/New Piskel.png")
respawn_img = pygame.image.load("img/New Piskel.png")
map_img = pygame.image.load("img/level layout map.png")
map_background_img = pygame.image.load("img/level background map.png")

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
arrow_img = pygame.transform.scale(pygame.image.load("img/Projectiles/arrow.png"), (10, 10))
spell_img = pygame.transform.scale(pygame.image.load("img/Projectiles/magic.png"), (50, 50))

# item images
health_img = pygame.transform.scale(pygame.image.load("img/Item/heart.png"), (20, 20))
max_health_img = pygame.transform.scale(pygame.image.load("img/Item/max_heart.png"), (20, 20))
mana_img = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (10, 10))
money_img = pygame.transform.scale(pygame.image.load("img/Item/coin.png"), (10, 10))
wall_jump_item = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (10, 10))
double_jump_item = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (10, 10))
emerald_img = pygame.transform.scale(pygame.image.load("img/Item/Emerald.png"), (10, 10))
ruby_img = pygame.transform.scale(pygame.image.load("img/Item/Ruby.png"), (10, 10))
sapphire_img = pygame.transform.scale(pygame.image.load("img/Item/Sapphire.png"), (10, 10))
item_dict = {
    "Health": health_img,
    "Mana": mana_img,
    "Money": money_img,
    "Walljump": wall_jump_item,
    "Doublejump": double_jump_item,
    "Emerald": emerald_img,
    "Ruby": ruby_img,
    "Sapphire": sapphire_img
}

# exit images
exitup_img = pygame.transform.scale(pygame.image.load("img/sign/upsign.png"), (tile_size, tile_size))
exitright_img = pygame.transform.scale(pygame.image.load("img/sign/rightsign.png"), (tile_size, tile_size))
exitdown_img = pygame.transform.scale(pygame.image.load("img/sign/downsign.png"), (tile_size, tile_size))
exitleft_img = pygame.transform.scale(pygame.image.load("img/sign/leftsign.png"), (tile_size, tile_size))

# font
font = pygame.font.SysFont(pygame.font.get_fonts()[41], 60)


def draw_bg():
    screen.blit(bg_img_list[current_world], (0, 0))


def draw_text(text, fonttype, color, xcoords, ycoords):
    txt_img = fonttype.render(text, True, color)
    screen.blit(txt_img, (xcoords, ycoords))


def reset_level():
    arrow_group.empty()
    spell_group.empty()
    item_group.empty()
    decoration_group.empty()
    lava_group.empty()
    exit_group.empty()
    enemy_group.empty()
    data = []
    for one_row in range(rows):
        p = [-1] * cols
        data.append(p)
    return data


class Button:
    def __init__(self, xcoords, ycoords, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = xcoords
        self.rect.y = ycoords
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
    def __init__(self, xcoords, ycoords):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 9
        self.max_health = 10
        self.speed = 20
        self.shoot_cooldown = 0
        self.cast_cooldown = 0
        self.direction = 1
        self.jump = False
        self.amount_jumps = 2
        self.in_air = True
        self.touching_wall = False
        self.wall_jump = False
        self.slide_factor = 0.5
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.wall_jump_cooldown = 60

        # load in images for player
        animation_types = ['Idle', 'Run', 'Jump', 'Shooting', 'Casting', 'Death']
        for animation in animation_types:
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/Player/{animation}'))
            for i in range(num_of_frames):
                player_img = pygame.image.load(f'img/Player/{animation}/{i}.png')
                player_img = pygame.transform.scale(player_img,
                                                    (player_img.get_width() * 2, player_img.get_height() * 2))
                temp_list.append(player_img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (xcoords, ycoords)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.mana = 10

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.cast_cooldown > 0:
            self.cast_cooldown -= 1

    def move(self, moving_left_direction, moving_right_direction):
        dx = 0
        dy = 0
        d_scroll_hor = 0
        d_scroll_ver = 0
        level_change_factor = 0
        previous_level_number = 0

        if moving_left_direction:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right_direction:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if not self.wall_jump and walljump_acquired:
            self.wall_jump_cooldown -= 1
        if self.wall_jump_cooldown <= 0:
            self.wall_jump_cooldown = 60
            self.wall_jump = True

        if not self.in_air or doublejump_acquired:
            if self.jump and not self.amount_jumps <= 0:
                if not self.touching_wall:
                    self.vel_y = -20
                    self.jump = False
                    self.in_air = True
                    if doublejump_acquired:
                        self.amount_jumps -= 1
                    else:
                        self.amount_jumps -= 2
                else:
                    if self.wall_jump and walljump_acquired:
                        self.vel_y = -20
                        self.jump = False
                        self.wall_jump = False
                        if not doublejump_acquired:
                            self.amount_jumps = 0

        if self.touching_wall:
            self.slide_factor = 0.5
        else:
            self.slide_factor = 1

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
            self.in_air = True
        dy += self.vel_y * self.slide_factor

        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.touching_wall = True
                if self.wall_jump:
                    self.amount_jumps = 1
                if self.direction > 0:
                    self.rect.right = one_tile[1].left - 1
                elif self.direction < 0:
                    self.rect.left = one_tile[1].right + 1
        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = d_scroll_ver
                    dy = one_tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.touching_wall = False
                    self.in_air = False
                    self.amount_jumps = 2
                    dy = one_tile[1].top - self.rect.bottom

        if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
            dx = 0

        if dx != 0:
            self.touching_wall = False
            if walljump_acquired:
                self.wall_jump_cooldown = 0

        if dy > 0:
            self.in_air = True

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # scrolling horizontal
        if (self.rect.right > screen_width - scroll_threshold_hor and
            total_hor_scroll < (world.level_length * tile_size) - screen_width) \
                or (self.rect.left < scroll_threshold_hor and total_hor_scroll > abs(dx)):
            self.rect.x -= int(dx)
            d_scroll_hor = -dx

        # scrolling vertical
        if self.rect.top < scroll_threshold_ver and not total_ver_scroll <= 0:
            self.rect.top = scroll_threshold_ver
            d_scroll_ver -= self.vel_y
        if self.rect.bottom > screen_height - scroll_threshold_ver and total_ver_scroll < (world.level_height * tile_size) - screen_height:
            self.rect.y -= int(dy)
            d_scroll_ver = -self.vel_y

        if pygame.sprite.spritecollide(self, exit_group, False):
            for exit_sign in exit_group:
                if exit_sign.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    level_change_factor = exit_sign.level_change
                    previous_level_number = exit_sign.direction
        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.health -= 1
        if pygame.sprite.spritecollide(self, lava_group, False):
            self.health = 0

        return d_scroll_hor, d_scroll_ver, level_change_factor, previous_level_number

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
            # shoot_fx.play()

    def cast(self):
        if self.cast_cooldown == 0:
            self.cast_cooldown = 100
            spell = Spell(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                          self.direction)
            spell_group.add(spell)
            self.mana -= 1
            # cast_fx.play()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, flying, xcoords, ycoords, enemy_type, vision_height, vision_width, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = health
        self.flying = flying
        self.speed = speed
        self.enemy_type = enemy_type
        self.direction = 1
        self.in_air = True
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        animation_types = ['Idle']
        for animation in animation_types:
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/Enemy/{self.enemy_type}/{animation}'))
            for i in range(num_of_frames):
                enemy_img = pygame.image.load(f'img/Enemy/{self.enemy_type}/{animation}/{i}.png')
                enemy_img = pygame.transform.scale(enemy_img, (enemy_img.get_width() * 2, enemy_img.get_height() * 2))
                temp_list.append(enemy_img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (xcoords, ycoords)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vision = pygame.Rect(0, 0, vision_width, vision_height)
        self.move_counter = 0

    def move(self):
        dx = 0
        dy = 0
        self.move_counter += 1
        if self.move_counter == 10 * (tile_size // self.speed):
            self.direction *= -1
            self.move_counter = 0

        if self.direction == -1:
            dx = -self.speed
            self.flip = True
        if self.direction == 1:
            dx = self.speed
            self.flip = False

        if not self.flying:
            self.vel_y += gravity
            if self.vel_y > 10:
                self.vel_y = 10
                self.in_air = True
            dy += self.vel_y

        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.direction *= -1
            if one_tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = one_tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    dy = one_tile[1].top - self.rect.bottom

        self.rect.x += int(dx)
        self.rect.y += int(dy)

    def update(self):
        self.move()
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World:
    def __init__(self):
        self.obstacle_list = []
        self.level_length = 0
        self.level_height = 0
        self.hor_off = 0
        self.ver_off = 0

    def process_data(self, data):
        self.level_length = len(data[0])
        self.level_height = len(data)
        for ycoords, one_row in enumerate(data):
            for xcoords, one_tile in enumerate(one_row):
                if one_tile == 0:
                    if xcoords + 1.5 <= 11:
                        self.hor_off = 0
                    else:
                        self.hor_off = -(xcoords - 8) * tile_size
                    if ycoords <= 5:
                        self.ver_off = 0
                    else:
                        self.ver_off = -(ycoords - 6) * tile_size
                if (one_tile == 1 or one_tile == 7 or one_tile == 11 or one_tile == 13 or one_tile == 15
                    or one_tile == 17) and previous_level == "Up":
                    if xcoords + 1.5 <= 11:
                        self.hor_off = 0
                    else:
                        self.hor_off = -(xcoords - 8) * tile_size
                    if ycoords <= 5:
                        self.ver_off = 0
                    else:
                        self.ver_off = -(ycoords - 6) * tile_size
                if (one_tile == 2 or one_tile == 8 or one_tile == 19 or one_tile == 21 or one_tile == 23
                    or one_tile == 25 or one_tile == 38) and previous_level == "Right":
                    if xcoords + 1.5 <= 11:
                        self.hor_off = 0
                    else:
                        self.hor_off = -(xcoords - 8) * tile_size
                    if ycoords <= 5:
                        self.ver_off = 0
                    else:
                        self.ver_off = -(ycoords - 6) * tile_size
                if (one_tile == 3 or one_tile == 9 or one_tile == 12 or one_tile == 14 or one_tile == 16
                    or one_tile == 18) and previous_level == "Down":
                    if xcoords + 1.5 <= 11:
                        self.hor_off = 0
                    else:
                        self.hor_off = -(xcoords - 8) * tile_size
                    if ycoords <= 5:
                        self.ver_off = 0
                    else:
                        self.ver_off = -(ycoords - 6) * tile_size
                if (one_tile == 4 or one_tile == 10 or one_tile == 20 or one_tile == 22 or one_tile == 24
                    or one_tile == 26 or one_tile == 39) and previous_level == "Left":
                    if xcoords + 1.5 <= 11:
                        self.hor_off = 0
                    else:
                        self.hor_off = -(xcoords - 8) * tile_size
                    if ycoords <= 5:
                        self.ver_off = 0
                    else:
                        self.ver_off = -(ycoords - 6) * tile_size
        for ycoords, one_row in enumerate(data):
            for xcoords, one_tile in enumerate(one_row):
                if one_tile >= 0:
                    image = tile_img_list[one_tile]
                    img_rect = image.get_rect()
                    img_rect.x = xcoords * tile_size + self.hor_off
                    img_rect.y = ycoords * tile_size + self.ver_off
                    tile_data = (image, img_rect)
                    if one_tile == 0:
                        player_character = Player(xcoords * tile_size + self.hor_off,
                                                  ycoords * tile_size + self.ver_off)
                    elif one_tile == 1:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", 1)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 2:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", 1)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 * player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 3:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", 1)
                        exit_group.add(exit_sign)

                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 4:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", 1)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 5:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 6:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 7:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", -1)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 8:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", -1)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 9:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", -1)
                        exit_group.add(exit_sign)

                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 10:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", -1)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 11:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", -4)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 12:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", 4)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 13:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", 5)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 14:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", -5)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 15:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", 7)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 16:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", -7)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 17:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", -13)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 18:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", 13)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 19:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", 5)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 * player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 20:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", -5)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 21:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", -2)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 * player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 22:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", 2)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 23:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", 2)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 * player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 24:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", -2)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 25:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", 4)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 * player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 26:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", -4)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 27:
                        pass
                    elif one_tile == 28:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 29:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 30:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 31:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 32:
                        item = Item(xcoords * tile_size + self.hor_off, ycoords * tile_size, "Health")
                        item_group.add(item)
                    elif one_tile == 33:
                        item = Item(xcoords * tile_size + self.hor_off, ycoords * tile_size, "Money")
                        item_group.add(item)
                    elif one_tile == 38:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", 45)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 * player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 39:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", -45)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif -2 <= one_tile <= -2:
                        lava = Lava(image, xcoords * tile_size + self.hor_off, ycoords * tile_size)
                        lava_group.add(lava)
                    elif -2 <= one_tile <= -2:
                        decoration = Decoration(image, xcoords * tile_size + self.hor_off, ycoords * tile_size)
                        decoration_group.add(decoration)
        return player_character

    def draw(self):
        for one_tile in self.obstacle_list:
            one_tile[1][0] += int(scroll_hor)
            one_tile[1][1] += int(scroll_ver)
            screen.blit(one_tile[0], one_tile[1])


class Exit(pygame.sprite.Sprite):
    def __init__(self, ex_img, xcoords, ycoords, direction, lvl_change):
        pygame.sprite.Sprite.__init__(self)
        self.image = ex_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (xcoords + tile_size // 2, ycoords + (tile_size - self.image.get_height()))
        self.direction = direction
        self.level_change = lvl_change

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, deco_img, xcoords, ycoords):
        pygame.sprite.Sprite.__init__(self)
        self.image = deco_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (xcoords + tile_size // 2, ycoords + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)


class Lava(pygame.sprite.Sprite):
    def __init__(self, lava_img, xcoords, ycoords):
        pygame.sprite.Sprite.__init__(self)
        self.image = lava_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (xcoords + tile_size // 2, ycoords + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)


class Item(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_dict[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (xcoords + tile_size // 2, ycoords + tile_size - self.image.get_height())

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Mana":
                pass
            elif self.item_type == "Money":
                pass
            elif self.item_type == "Walljump":
                walljump_acquired = True
            elif self.item_type == "Doublejump":
                doublejump_acquired = True
            elif self.item_type == "Emerald":
                emerald_acquired = True
            elif self.item_type == "Ruby":
                ruby_acquired = True
            elif self.item_type == "Sapphire":
                sapphire_acquired = True

            self.kill()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        if direction > 0:
            self.image = arrow_img
        else:
            self.image = pygame.transform.flip(arrow_img, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (xcoords, ycoords)
        self.direction = direction

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        self.rect.x += self.direction * self.speed
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect):
                self.kill()


class Spell(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 6
        if direction > 0:
            self.image = spell_img
        else:
            self.image = pygame.transform.flip(spell_img, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (xcoords, ycoords)
        self.direction = direction
        self.lifetime = 60

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        self.rect.x += self.direction * self.speed
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect):
                self.kill()


# sprite groups
arrow_group = pygame.sprite.Group()
spell_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

start_btn = Button(screen_width // 2 - 130, screen_height // 2 - 150, start_img)
exit_btn = Button(screen_width // 2 - 130, screen_height // 2 + 50, exit_img)
respawn_btn = Button(screen_width // 2 - 130, screen_height // 2 - 150, respawn_img)

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
total_hor_scroll = -world.hor_off
total_ver_scroll = -world.ver_off

run = True
while run:
    if game_started:
        if 0 <= level <= 6:
            current_world = 0
        elif 7 <= level <= 14:
            current_world = 1
        elif 15 <= level <= 26:
            current_world = 2
        elif 27 <= level <= 37:
            current_world = 3
        elif 38 <= level <= 48:
            current_world = 4
        draw_bg()
        world.draw()
        for x in range(player.max_health):
            screen.blit(max_health_img, (90 + (x * 20), 40))
        for x in range(player.health):
            screen.blit(health_img, (90 + (x * 20), 40))

        for enemy in enemy_group:
            enemy.update()
            enemy.draw()

        # update + draw groups
        arrow_group.update()
        spell_group.update()
        item_group.update()
        decoration_group.update()
        lava_group.update()
        exit_group.update()
        arrow_group.draw(screen)
        spell_group.draw(screen)
        item_group.draw(screen)
        decoration_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)

        scroll_hor, scroll_ver, level_change, previous_level = player.move(moving_left, moving_right)
        total_hor_scroll -= scroll_hor
        total_ver_scroll -= scroll_ver
        if player.alive:
            player.update()
            player.draw()
            if cast:
                player.cast()
                player.update_action(4)
            if shoot:
                player.shoot()
                player.update_action(3)
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)

            if map_menu:
                screen.blit(map_background_img, (0, 0))
                screen.blit(map_img, (0, 0))

            if level_change != 0:
                total_hor_scroll = 0
                total_ver_scroll = 0
                level += level_change
                level_change = 0
                world_data = reset_level()
                with open(f'level_data/level_data{level}.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player = world.process_data(world_data)
                total_hor_scroll = -world.hor_off
                total_ver_scroll = -world.ver_off

        else:
            scroll_ver = 0
            scroll_hor = 0
            draw_text("You died", font, (0, 0, 0), 250, 60)
            if respawn_btn.draw():
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
                total_hor_scroll = -world.hor_off
                total_ver_scroll = -world.ver_off
            elif exit_btn.draw():
                run = False
    else:
        screen.fill((50, 50, 50))
        draw_text("A Tiny Little Game", font, (0, 0, 0), 250, 60)
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
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_z and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_a:
                shoot = True
            if event.key == pygame.K_s:
                cast = True
            if event.key == pygame.K_m:
                map_menu = True
            if event.key == pygame.K_DELETE:
                player.alive = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_z:
                player.jump = False
            if event.key == pygame.K_a:
                shoot = False
            if event.key == pygame.K_s:
                cast = False
            if event.key == pygame.K_m:
                map_menu = False

    clock.tick(fps)
    pygame.display.update()

pygame.quit()
