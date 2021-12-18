import pygame
from pygame import mixer
import os
import csv
import random
import math

pygame.init()
mixer.init()

# frame rate
clock = pygame.time.Clock()
fps = 60

# screen size
screen_width = 1024
screen_height = 576

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Re:Birth")

tile_size = 64
tile_types = 44
cols = 48
rows = 27
game_over = False
previous_level = "Left"
level = 0
current_world = 0
world_types = 3
game_started = False
hor_offset = 0
ver_offset = 0
player_health = 10
player_max_health = 10
wallet = 0

gravity = 0.75

# action variables
moving_left = False
moving_right = False
shoot = False
cast = False
attack = False
walljump_acquired = False
doublejump_acquired = False
emerald_acquired = False
ruby_acquired = False
sapphire_acquired = False
map_menu = False
gathered_item_list = []

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
money_img = pygame.transform.scale(pygame.image.load("img/Item/coin.png"), (20, 20))
wall_jump_item = pygame.transform.scale(pygame.image.load("img/Item/Wall_jump.png"), (tile_size, tile_size))
double_jump_item = pygame.transform.scale(pygame.image.load("img/Item/Double_jump.png"), (tile_size, tile_size))
emerald_img = pygame.transform.scale(pygame.image.load("img/Item/Emerald.png"), (tile_size, tile_size))
ruby_img = pygame.transform.scale(pygame.image.load("img/Item/Ruby.png"), (tile_size, tile_size))
sapphire_img = pygame.transform.scale(pygame.image.load("img/Item/Sapphire.png"), (tile_size, tile_size))
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
    for _ in range(rows):
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
        self.health = player_health
        self.max_health = player_max_health
        self.speed = 8
        self.shoot_cooldown = 0
        self.cast_cooldown = 0
        self.melee_cooldown = 0
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
        self.invincibility = 60

        # load in images for player
        animation_types = ['Idle', 'Run', 'Jump', 'Shooting', 'Casting', 'Death', 'Touching_wall', 'Melee']
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
        if self.melee_cooldown > 0:
            self.melee_cooldown -= 1

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
                if walljump_acquired:
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
                    dy = one_tile[1].bottom - self.rect.top + 5
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
        if self.rect.bottom > screen_height - scroll_threshold_ver and\
                total_ver_scroll < (world.level_height * tile_size) - screen_height:
            self.rect.y -= int(dy)
            d_scroll_ver = -self.vel_y

        if pygame.sprite.spritecollide(self, exit_group, False):
            for exit_sign in exit_group:
                if exit_sign.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    level_change_factor = exit_sign.level_change
                    previous_level_number = exit_sign.direction

        if self.invincibility > 0:
            self.invincibility -= 1
        if pygame.sprite.spritecollide(self, enemy_group, False) and self.invincibility <= 0:
            self.health -= 1
            self.invincibility = 60
        if pygame.sprite.spritecollide(self, lava_group, False):
            self.health = 0

        return d_scroll_hor, d_scroll_ver, level_change_factor, previous_level_number

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def melee(self):
        if self.melee_cooldown == 0:
            self.melee_cooldown = 10
            self.rect.centerx -= 5 * self.direction
            if enemy in enemy_group:
                if math.sqrt(((enemy.rect.centerx - self.rect.centerx) ** 2) +
                             (enemy.rect.centery - self.rect.centery) ** 2) < (2 * tile_size):
                    if enemy.rect.centerx > self.rect.centerx * self.direction:
                        enemy.health -= 10
                        self.rect.centerx -= 20 * self.direction

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
    def __init__(self, flying, xcoords, ycoords, enemy_type, vision_height, vision_width):
        pygame.sprite.Sprite.__init__(self)
        self.world = 1
        self.alive = True
        self.health = 5
        self.flying = flying
        self.speed = 4
        self.enemy_type = enemy_type
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, vision_width, vision_height)
        self.idling = False
        self.idling_counter = 0
        if current_world == 0:
            self.world = 0
        elif current_world == 2:
            self.world = 1
        elif current_world == 3:
            self.world = 2
        elif current_world == 4:
            self.world = 3
        if self.world != 1:
            animation_types = ['Idle']
            for animation in animation_types:
                temp_list = []
                # count number of files in the folder
                num_of_frames = len(os.listdir(f'img/Enemy/Enemy{self.enemy_type}/World{self.world}/{animation}'))
                for i in range(num_of_frames):
                    enemy_img = pygame.transform.scale(
                        pygame.image.load(f'img/Enemy/Enemy{self.enemy_type}/World{self.world}/{animation}/{i}.png'),
                        (tile_size, tile_size))
                    temp_list.append(enemy_img)
                self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.index]
            self.rect = self.image.get_rect()
            self.rect.center = (xcoords, ycoords)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        self.move_counter = 0

    def move(self, mov_left, mov_right):
        dx = 0
        dy = 0
        if mov_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if mov_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if not self.flying:
            self.vel_y += gravity
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if one_tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = one_tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    dy = one_tile[1].top - self.rect.bottom

        self.rect.x += int(dx)
        self.rect.y += int(dy)

    def ai(self):
        if self.alive and player.alive:
            if pygame.sprite.spritecollide(self, spell_group, True):
                self.health -= 5
            if pygame.sprite.spritecollide(self, arrow_group, True):
                self.health -= 1
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(player.rect):
                self.attack()
                self.idling = True
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(0)  # 1: run
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx, self.rect.centery)

                    if self.move_counter > tile_size:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

            self.rect.x += int(scroll_hor)
            self.rect.y += int(scroll_ver)

    def attack(self):
        if self.enemy_type == 1:
            if -2 <= (self.rect.centery - player.rect.top) <= 2:
                self.rect.centery = player.rect.top
            elif self.rect.centery > player.rect.top:
                self.rect.centery -= 2
            elif self.rect.centery < player.rect.top:
                self.rect.centery += 2
            if self.rect.centerx > player.rect.centerx:
                self.move(True, False)
            elif self.rect.centerx < player.rect.centerx:
                self.move(False, True)

        elif self.enemy_type == 2:
            pass

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
            self.update_action(0)

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

    def update(self):
        self.update_animation()
        self.check_alive()
        if not self.alive:
            self.kill()

    def draw(self):
        if self.alive:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Npc(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, character):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f'img/NPC/{character}.png')
        self.img = pygame.transform.scale(self.img,
                                          (self.img.get_width() * 2, self.img.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (xcoords, ycoords)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.update_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        screen.blit(self.img, self.rect)


class Boss(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, which_world):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = 2
        self.health = 5
        self.world = which_world
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        animation_types = ['Idle', 'Attack1', 'Attack2', 'Attack3', 'Death']
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
        self.update_time = pygame.time.get_ticks()

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
            self.update_action(0)

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

    def update(self):
        self.update_animation()
        self.check_alive()
        if not self.alive:
            self.kill()

    def draw(self):
        if self.alive:
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
                        one_enemy = Enemy(True, xcoords * tile_size + self.hor_off,
                                          ycoords * tile_size + self.ver_off, 1, 300, 600)
                        enemy_group.add(one_enemy)
                    elif one_tile == 28:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 29:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 30:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 31:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 32:
                        one_item = Item(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, "Health")
                        item_group.add(one_item)
                    elif one_tile == 33:
                        one_item = Item(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, "Money")
                        item_group.add(one_item)
                    elif one_tile == 34:
                        npc = Npc(xcoords * tile_size + self.hor_off, ycoords * tile_size + self.ver_off, 'joseph')
                        npc_group.add(npc)
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
                    elif one_tile == 40:
                        lava = Lava(image, xcoords * tile_size + self.hor_off, ycoords * tile_size + self.ver_off)
                        lava_group.add(lava)
                    elif one_tile == 41:
                        lava = Lava(image, xcoords * tile_size + self.hor_off, ycoords * tile_size + self.ver_off)
                        lava_group.add(lava)
                    elif one_tile == 42:
                        one_item = Item(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, "Doublejump")
                        item_group.add(one_item)
                    elif one_tile == 43:
                        one_item = Item(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, "Walljump")
                        item_group.add(one_item)
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
        self.rect.midtop = (xcoords + tile_size // 2, ycoords)

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
        self.walljump_acquired = False
        self.doublejump_acquired = False
        self.emerald_acquired = False
        self.ruby_acquired = False
        self.sapphire_acquired = False

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
                self.walljump_acquired = True
            elif self.item_type == "Doublejump":
                self.doublejump_acquired = True
            elif self.item_type == "Emerald":
                self.emerald_acquired = True
            elif self.item_type == "Ruby":
                self.ruby_acquired = True
            elif self.item_type == "Sapphire":
                self.sapphire_acquired = True
            elif self.item_type == "Coin":
                wallet += 1
            self.kill()
        return [self.walljump_acquired, self.doublejump_acquired, self.emerald_acquired,
                self.ruby_acquired, self.sapphire_acquired]


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
npc_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

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
            enemy.ai()
            enemy.update()
            enemy.draw()

        for Npc in npc_group:
            Npc.update()
            Npc.draw()

        # update + draw groups
        arrow_group.update()
        spell_group.update()
        for item in item_group:
            gathered_item_list = item.update()
            if not walljump_acquired:
                walljump_acquired = gathered_item_list[0]
            if not doublejump_acquired:
                doublejump_acquired = gathered_item_list[1]
            if not emerald_acquired:
                emerald_acquired = gathered_item_list[2]
            if not ruby_acquired:
                ruby_acquired = gathered_item_list[3]
            if not sapphire_acquired:
                sapphire_acquired = gathered_item_list[4]
        decoration_group.update()
        lava_group.update()
        exit_group.update()
        npc_group.update()
        boss_group.update()
        arrow_group.draw(screen)
        spell_group.draw(screen)
        item_group.draw(screen)
        decoration_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        npc_group.draw(screen)
        boss_group.draw(screen)

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
            if attack:
                player.melee()
                player.update_action(7)
            if player.in_air:
                player.update_action(2)
            if player.touching_wall and player.in_air:
                player.update_action(6)
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
                player_health = player.health
                player_max_health = player.max_health
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
                player_health = player_max_health
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
        draw_text("Re: Birth", font, (0, 0, 0), 250, 60)
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
            if event.key == pygame.K_x:
                attack = True

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
            if event.key == pygame.K_x:
                attack = False

    clock.tick(fps)
    pygame.display.update()

pygame.quit()
