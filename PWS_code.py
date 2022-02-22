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

pos_dict = {0: (340, 290), 1: (390, 290), 2: (440, 290), 3: (440, 320), 4: (490, 290), 5: (540, 290), 6: (590, 290), 7: (440, 270), 8: (490, 270), 9: (540, 270), 10: (590, 270), 11: (390, 270), 12: (350, 260), 13: (310, 230), 14: (270, 230), 15: (640, 260), 16: (690, 260), 17: (740, 260), 18: (740, 230), 19: (790, 210), 20: (840, 230), 21: (840, 260), 22: (670, 230), 23: (700, 200), 24: (730, 180), 25: (780, 180), 26: (780, 120), 27: (270, 290), 28: (220, 310), 29: (270, 330), 30: (270, 360), 31: (310, 360), 32: (220, 360), 33: (170, 360), 34: (170, 390), 35: (210, 390), 36: (260, 390), 37: (310, 390), 38: (160, 420), 39: (160, 450), 40: (490, 450), 41: (490, 410), 42: (490, 390), 43: (540, 390), 44: (590, 390), 45: (640, 390), 46: (640, 360), 47: (640, 330), 48: (540, 330)}


# screen size
screen_width = 1024
screen_height = 576

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Re:Birth")

# game variables
tile_size = 64
tile_types = len(os.listdir(f'img/Tile/'))
cols = 48
rows = 27
game_over = False
previous_level = "Left"
level = 0
current_world = 0
world_types = 5
game_started = False
hor_offset = 0
ver_offset = 0
player_health = 10
player_max_health = 10
player_mana = 10
player_max_mana = 10
wallet = 0
talking_phase = 1
gathered_item_list = []
gravity = 0.75

# action and menu variables
moving_left = False
moving_right = False
shoot = False
cast = False
attack = False
skip_text = False
walljump_acquired = False
doublejump_acquired = False
emerald_acquired = False
ruby_acquired = False
sapphire_acquired = False
map_menu = False
pause_menu = False
settings = False
inventory = False
shop = False
controls = False
ending = False
music_started = False

# scroll variables
scroll_threshold_hor = 4 * tile_size
scroll_threshold_ver = 2 * tile_size
scroll_hor = 0
scroll_ver = 0
scroll_speed = 1
total_hor_scroll = 0
total_ver_scroll = 0

volume = 0.5
pygame.mixer.music.load("audio/Title screen OST.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1, 0.0, 4000)
# load music and sounds
music_index = -1
jump_fx = pygame.mixer.Sound("audio/jump.wav")
jump_fx.set_volume(volume)
cast_fx = pygame.mixer.Sound("audio/cast.wav")
cast_fx.set_volume(volume)
shoot_fx = pygame.mixer.Sound("audio/shoot.wav")
shoot_fx.set_volume(volume)
hurt_fx = pygame.mixer.Sound("audio/hurt.wav")
shoot_fx.set_volume(volume)
sword_fx = pygame.mixer.Sound("audio/sword.wav")
shoot_fx.set_volume(volume)

# images
# ending images
ending0_img = pygame.transform.scale(pygame.image.load("img/EndScenes/0.png"), (screen_width, screen_height))
ending1_img = pygame.transform.scale(pygame.image.load("img/EndScenes/1.png"), (screen_width, screen_height))
ending2_img = pygame.transform.scale(pygame.image.load("img/EndScenes/2.png"), (screen_width, screen_height))
ending3_img = pygame.transform.scale(pygame.image.load("img/EndScenes/3.png"), (screen_width, screen_height))
ending4_img = pygame.transform.scale(pygame.image.load("img/EndScenes/4.png"), (screen_width, screen_height))
ending5_img = pygame.transform.scale(pygame.image.load("img/EndScenes/5.png"), (screen_width, screen_height))

# title screen image
title_img = pygame.image.load("img/Menu/title screen.png")

# button images
start_img = pygame.image.load("img/Button/start.png")
exit_img = pygame.image.load("img/Button/exit.png")
respawn_img = pygame.image.load("img/Button/respawn.png")
settings_img = pygame.image.load("img/New Piskel.png")
volume_up_img = pygame.image.load("img/New Piskel.png")
volume_down_img = pygame.image.load("img/New Piskel.png")
inventory_btn_img = pygame.image.load("img/New Piskel.png")
save_img = pygame.image.load("img/Button/save.png")
load_img = pygame.image.load("img/Button/load.png")

# menu images
map_img = pygame.image.load("img/level layout map.png")
map_background_img = pygame.image.load("img/level background map.png")
inventory_img = pygame.image.load("img/Menu/inventory.png")
controls_img = pygame.image.load("img/Menu/Controls.png")
game_over_img = pygame.image.load("img/Menu/death screen.png")
speech_block_img = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (screen_width, screen_height - 480))
shop_img = pygame.transform.scale(pygame.image.load("img/New Piskel.png"), (screen_width, screen_height - 480))

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
arrow_img = pygame.transform.scale(pygame.image.load("img/Projectiles/arrow.png"), (20, 20))
spell_img = pygame.transform.scale(pygame.image.load("img/Projectiles/magic.png"), (50, 50))
fire_attack_img = pygame.transform.scale(pygame.image.load("img/Projectiles/fire_attack.png"), (116, 98))
ball_attack_img = pygame.transform.scale(pygame.image.load("img/Projectiles/ball_attack.png"), (50, 50))
wall_attack_img = pygame.transform.scale(pygame.image.load("img/Projectiles/wall_attack.png"), (32, 64))
slimeball_img = pygame.transform.scale(pygame.image.load("img/Projectiles/slimeball.png"), (40, 40))
desert_slimeball_img = pygame.transform.scale(pygame.image.load("img/Projectiles/desertslimeball.png"), (40, 40))
lava_slimeball_img = pygame.transform.scale(pygame.image.load("img/Projectiles/lavaslimeball.png"), (40, 40))
snow_slimeball_img = pygame.transform.scale(pygame.image.load("img/Projectiles/snowslimeball.png"), (40, 40))

# item images
health_img = pygame.transform.scale(pygame.image.load("img/Item/heart.png"), (20, 20))
max_health_img = pygame.transform.scale(pygame.image.load("img/Item/max_heart.png"), (20, 20))
mana_img = pygame.transform.scale(pygame.image.load("img/Item/mana.png"), (20, 20))
max_mana_img = pygame.transform.scale(pygame.image.load("img/Item/max_mana.png"), (20, 20))
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


def draw_text(text, fonttype, color, xcoords, ycoords, size):
    txt_img = fonttype.render(text, True, color)
    txt_img = pygame.transform.scale(txt_img, (txt_img.get_width() * size, txt_img.get_height() * size))
    screen.blit(txt_img, (xcoords, ycoords))


def reset_level():
    arrow_group.empty()
    spell_group.empty()
    item_group.empty()
    decoration_group.empty()
    lava_group.empty()
    exit_group.empty()
    enemy_group.empty()
    npc_group.empty()
    boss_group.empty()
    slime_group.empty()
    fire_attack_group.empty()
    ball_attack_group.empty()
    wall_attack_group.empty()
    data = []
    for _ in range(rows):
        p = [-1] * cols
        data.append(p)
    return data


def play_music(level_number):
    music = music_index
    if ((0 <= level_number <= 5) or (8 <= level_number <= 20) or (22 <= level_number <= 30) or (32 <= level_number <= 36) or (38 <= level_number <= 49)) and music != 0:
        pygame.mixer.music.load("audio/General bg OST.mp3")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 4000)
        music = 0
    elif (level_number == 6 or level_number == 26 or level_number == 37 or level_number == 48) and music != 1:
        pygame.mixer.music.load("audio/Eerie OST.mp3")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 4000)
        music = 1
    elif level_number == 7 and music != 2:
        pygame.mixer.music.load("audio/Town OST.mp3")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 4000)
        music = 2
    elif level_number == 21 or level_number == 31 and music != 3:
        pygame.mixer.music.load("audio/Gem Acquirement OST.mp3")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 4000)
        music = 3
    elif level_number == 50 and music != 4:
        pygame.mixer.music.load("audio/Less eerie OST.mp3")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 4000)
        music = 4

    return music


def fade(window): 
    fade = pygame.Surface((window.get_width(), window.get_height()))
    fade.fill((0, 0, 0))
    for alpha in range(0, 60):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


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
        self.mana = player_mana
        self.max_mana = player_max_mana
        self.wallet = wallet
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
        self.invincibility = 0

        # load in images for player
        animation_types = ['Idle', 'Run', 'Jump', 'Shooting', 'Casting', 'Death', 'Touching_wall', 'Melee', 'Damage']
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
        self.attacking = False

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
                    jump_fx.play()
                    if doublejump_acquired:
                        self.amount_jumps -= 1
                    else:
                        self.amount_jumps -= 2
                else:
                    if self.wall_jump and walljump_acquired:
                        self.vel_y = -20
                        self.jump = False
                        self.wall_jump = False
                        jump_fx.play()
                        if not doublejump_acquired:
                            self.amount_jumps = 0

        if self.touching_wall and self.vel_y > 0:
            self.slide_factor = 0.5
        else:
            self.slide_factor = 1

        self.vel_y += gravity * self.slide_factor
        if self.vel_y > 10 * self.slide_factor:
            self.vel_y = 10 * self.slide_factor
            self.in_air = True
        dy += self.vel_y

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
            if one_tile[1].colliderect(self.rect.x, self.rect.y + dy + gravity, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = d_scroll_ver
                    dy = one_tile[1].bottom - self.rect.top + 5
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.touching_wall = False
                    self.in_air = False
                    self.amount_jumps = 2
                    dy = one_tile[1].top - self.rect.bottom - 0.1

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

        # exit
        if pygame.sprite.spritecollide(self, exit_group, False):
            for exit_sign in exit_group:
                if exit_sign.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    level_change_factor = exit_sign.level_change
                    previous_level_number = exit_sign.direction

        # collision checks
        if self.invincibility > 0:
            self.invincibility -= 1
            self.update_action(8)
        if self.alive:
            if pygame.sprite.spritecollide(self, enemy_group, False) and self.invincibility <= 0:
                self.health -= 1
                self.invincibility = 60
                hurt_fx.play()
            if pygame.sprite.spritecollide(self, slime_group, False) and self.invincibility <= 0:
                self.health -= 1
                self.invincibility = 60
                hurt_fx.play()
            if pygame.sprite.spritecollide(self, lava_group, False):
                self.health = 0
                hurt_fx.play()
            if pygame.sprite.spritecollide(self, fire_attack_group, False) and self.invincibility <= 0:
                self.health -= 1
                self.invincibility = 60
                hurt_fx.play()
            if pygame.sprite.spritecollide(self, ball_attack_group, False) and self.invincibility <= 0:
                self.health -= 1
                self.invincibility = 60
                hurt_fx.play()
            if pygame.sprite.spritecollide(self, wall_attack_group, False) and self.invincibility <= 0:
                self.health -= 1
                self.invincibility = 60
                hurt_fx.play()

        return d_scroll_hor, d_scroll_ver, level_change_factor, previous_level_number

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def melee(self):
        if self.melee_cooldown == 0:
            sword_fx.play()
            self.attacking = True
            self.invincibility = 0
            self.melee_cooldown = 20
            for enemy in enemy_group:
                if math.sqrt(((enemy.rect.centerx - self.rect.centerx) ** 2) +
                             (enemy.rect.centery - self.rect.centery) ** 2) < (2 * tile_size):
                    if enemy.rect.centerx > self.rect.centerx * self.direction:
                        enemy.health -= 10
            for boss in boss_group:
                if math.sqrt(((boss.rect.centerx - self.rect.centerx) ** 2) +
                             (boss.rect.centery - self.rect.centery) ** 2) < (2 * tile_size):
                    if boss.rect.centerx > self.rect.centerx * self.direction:
                        boss.health -= 10
        else:
            self.attacking = False

    def check_alive(self):
        if player.rect.y > screen_height * 3:
            self.health = 0
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
            self.index = 0

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            arrow = Arrow(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                          self.direction)
            arrow_group.add(arrow)
            shoot_fx.play()

    def cast(self):
        if self.cast_cooldown == 0 and self.mana > 0:
            self.cast_cooldown = 100
            spell = Spell(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                          self.direction)
            spell_group.add(spell)
            self.mana -= 1
            cast_fx.play()

    def draw(self):
        if self.attacking and self.direction == -1:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - pygame.image.load("img/Player/Melee/0.png").get_width() - 29, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, flying, xcoords, ycoords, enemy_type, vision_height, vision_width):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.flying = flying
        if enemy_type == 1:
            self.speed = 3
            self.health = 20
        elif enemy_type == 2:
            self.speed = 2
            self.health = 30
        self.enemy_type = enemy_type
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.slime_cooldown = 0
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
        if current_world != 1:
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
                self.health -= 10
            if pygame.sprite.spritecollide(self, arrow_group, True):
                self.health -= 5
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
            if self.slime_cooldown <= 0:
                self.slime_cooldown = 120
                slime = Slime(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                              self.direction, self.world)
                slime_group.add(slime)
            if self.rect.centerx > player.rect.centerx:
                self.move(True, False)
            elif self.rect.centerx < player.rect.centerx:
                self.move(False, True)
            self.slime_cooldown -= 1

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
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Npc(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, character):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'img/NPC/{character}.png')
        if character == "portalman":
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 2, self.image.get_height() * 2))
            self.rect = self.image.get_rect()
            self.rect.center = (xcoords, ycoords)
        else:
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 2.5, self.image.get_height() * 2.5))
            self.rect = self.image.get_rect()
            self.rect.center = (xcoords + 0.375 * tile_size, ycoords + 0.375 * tile_size)
        self.character = character
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vision = pygame.Rect(0, 0, 200, 300)
        self.update_time = pygame.time.get_ticks()
        self.text = 0
        self.skip_text = skip_text
        self.check_skip_cooldown = 10
        self.level_changer = 0
        self.talking_phase = talking_phase
        self.shop = False

    def interact(self):
        if player.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
            if self.character == "joseph":
                if self.talking_phase == 1:
                    while True:
                        if self.skip_text and self.check_skip_cooldown <= 0:
                            self.check_skip_cooldown = 10
                            self.text += 1
                            self.skip_text = False
                        else:
                            self.check_skip_cooldown -= 1
                        if self.text == 0:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("?:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Oh, hello there! You don't seem to be from here.", font, (255, 255, 255), 10, 510, 0.3)
                            draw_text("   Are you lost traveller?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 1:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Uhm.. hello.. I’m not sure either, my head hurts...", font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   What is this place? Who are you?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 2:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("?:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   This is my hometown, isn’t it beautiful? It’s nice to meet you, I’m joseph!", font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   Do you perhaps... remember your name?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 3:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   ...ouch..I.. I think it’s.. Adonis?", font, (255, 255, 255), 10, 510, 0.3)
                        elif self.text == 4:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   What a wonderful name, it sounds unfamiliar to me though.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   It does not sound like it came from any of our regions.. ", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 5:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Do you remember where you’re from? I’d like to help you get back home!",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   It is dangerous out there.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 6:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   I don’t recognize anything here.", font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   I just encountered monsters that attacked me on the way here.. is this.. Earth?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 7:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Earth? I’m sorry, this is Elysium.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   Did you maybe remember it wrong?", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 8:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   What? No! I am from planet Earth.", font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   What is this place?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 9:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Hmm…",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 10:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   This is Elysium, the world that was once known for its lush nature and prosperous cities.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   It used to be bustling with activity, but it’s now all been reduced to empty regions", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 11:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   with extreme weather and monsters swarming around after the calamity hit.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   This is the only town left unscathed.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 12:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Wow, that’s.. a lot to take in. I need a moment..", font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   I’m really sorry for your loss, but how do I get back?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 13:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   That’s understandable, take your time.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   I think I might know someone that does know how to bring you back, but it will take a little bit of traveling.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 14:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   It’s quite dangerous as well, with the monsters roaming around.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   I’m not sure if it’d be wise for you to travel in this condition.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 15:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   It’s alright, please.. tell me where I can find them.", font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   I just want to go home.", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 16:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   He’s located in the underground caves you just came from.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   You’ll have to go back down and go to the right.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 17:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Thank you, err.. sir Joseph.", font, (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 18:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   It’s fine, you can just call me uncle Joseph.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 19:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   I unfortunately cannot go into the underground caves with you, so I hope you stay safe.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   See you again, Adonis.", font,
                                      (255, 255, 255), 10, 530, 0.3)

                        break
                elif self.talking_phase == 2:
                    while True:
                        if self.skip_text and self.check_skip_cooldown <= 0:
                            self.check_skip_cooldown = 10
                            self.text += 1
                            self.skip_text = False
                        else:
                            self.check_skip_cooldown -= 1
                        if self.text == 0:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   You’re back, Adonis! I’m glad to see you are alive and well.", font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   Did you find him?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 1:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Uncle Joseph, you do not realize how glad I am to see you again.", font, (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   Yes, I did find him, he’s.. eccentric. He was kind of rude too.", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 2:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Hahaha, that is unfortunate.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   What did he say, did he find a way to help you get back?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 3:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   He said something about getting an emerald from the desert,", font, (255, 255, 255), 10, 510, 0.3)
                            draw_text("   a ruby from the volcano and the sapphire from the snowy plains.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 4:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   He never told me where those places are though..", font, (255, 255, 255), 10, 510, 0.3)
                        elif self.text == 5:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Haha, that does indeed sound like him! He must be going senile.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   I'll tell you instead.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 6:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   If you head to the right from this town, you'll arrive at the pyramid in the desert.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 7:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   If you head left from here after you return from the desert,",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   you'll arrive at the volcano.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 7:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Joseph:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   The snowy plains are located south of the volcanic region.",
                                      font, (255, 255, 255), 10,
                                      510, 0.3)
                            draw_text("   I hope this helps you. Have a safe travel, Adonis!", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 1:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Thank you so much uncle Joseph,", font, (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   I'll be on my way now!", font, (255, 255, 255), 10, 530, 0.3)
                        break
            elif self.character == "portalman":
                if self.talking_phase == 1:
                    while True:
                        if self.skip_text and self.check_skip_cooldown <= 0:
                            self.check_skip_cooldown = 10
                            self.text += 1
                            self.skip_text = False
                        else:
                            self.check_skip_cooldown -= 1
                        if self.text == 0:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Hello?", font,
                                      (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 1:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Ah! Hello, my boy. I was waiting for you.", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   So, you seek to return to your own world?", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 2:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Huh? What? Uh- yeah- yes, sure?", font,
                                      (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 3:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Great, let’s get a move on. Time is ticking.", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   I don’t have time to engage in idle chit-chat,", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 4:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("    so let me just see here.. ", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   where were you from again?", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 5:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Earth?", font,
                                      (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 6:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("    Of course, of course.. What is your name?", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                        elif self.text == 7:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Adonis.", font,
                                      (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 8:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("    You don’t remember your full name?", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                        elif self.text == 9:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   No.. ouch.. by the way, do you guys have a hospital somewhere?", font,
                                      (255, 255, 255), 10,
                                      510, 0.3)
                        elif self.text == 10:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Oh no! How unfortunate,", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   anyway..", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 11:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Aha! Here it is, okay..", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   So in order for me to be able to open up the portal,", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 12:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   which you can use to return to Earth,", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   you’ll have to bring me 3 gems:", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 13:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   the emerald from the pyramid,", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                        elif self.text == 14:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   the ruby from the volcano and", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                        elif self.text == 15:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   the sapphire from the snowy plains.", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                        elif self.text == 16:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Now, off you go, if you want to return home as fast as possible.", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("   I haven’t got all day! I’m getting older by the minute,", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 17:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   I might be on my last breath by the time", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                            draw_text("    you decide to make your merry way back.", font,
                                      (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 18:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Sheesh, okay, calm down.. I’m already leaving.", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                        elif self.text == 19:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   ..Wait, he didn’t tell me where to go. I guess I’ll just go back to uncle Joseph.", font,
                                      (255, 255, 255),
                                      10,
                                      510, 0.3)
                        else:
                            self.talking_phase += 1
                        break
                elif self.talking_phase == 2:
                    while True:
                        if self.skip_text and self.check_skip_cooldown <= 0:
                            self.check_skip_cooldown = 10
                            self.text += 1
                            self.skip_text = False
                        else:
                            self.check_skip_cooldown -= 1
                        if emerald_acquired and ruby_acquired and sapphire_acquired:
                            if self.text == 0:
                                draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("   Wizard, I’ve come to bargain.", font,
                                          (255, 255, 255), 10,
                                          510, 0.3)
                            elif self.text == 1:
                                draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("   What? Wizard? I’ll act like I never heard that.", font,
                                          (255, 255, 255),
                                          10,
                                          510, 0.3)
                                draw_text("   So, I presume you’ve got the gems.", font,
                                          (255, 255, 255), 10, 530, 0.3)
                            if self.text == 2:
                                draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("   Yes, I have the gems,", font,
                                          (255, 255, 255), 10,
                                          510, 0.3)
                                draw_text("   which you forgot to give me the directions for.", font,
                                          (255, 255, 255), 10, 530, 0.3)
                            elif self.text == 3:
                                draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("    ... ", font,
                                          (255, 255, 255),
                                          10,
                                          510, 0.3)
                                draw_text("   Anyway.", font,
                                          (255, 255, 255), 10, 530, 0.3)
                            elif self.text == 4:
                                draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("    Hand them over so I can start the spell on opening the portal. ", font,
                                          (255, 255, 255),
                                          10,
                                          510, 0.3)
                                draw_text("   It will open in the next room.", font,
                                          (255, 255, 255), 10, 530, 0.3)
                            elif self.text == 5:
                                draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("   Alright, here are the emerald, ruby and the sapphire.", font,
                                          (255, 255, 255), 10,
                                          510, 0.3)
                            elif self.text == 6:
                                draw_text("Portalman:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("    Great, you may now pass. I hope you have a safe journey", font,
                                          (255, 255, 255),
                                          10,
                                          510, 0.3)
                            elif self.text == 7:
                                draw_text("You:", font, (255, 255, 255), 10, 490, 0.3)
                                draw_text("   Uhm… alright. Thanks, I guess.", font,
                                          (255, 255, 255), 10,
                                          510, 0.3)
                            self.level_changer = 1
                        else:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("You haven't collected everything", font, (255, 255, 255), 10, 500,
                                      0.5)
                        break
            elif self.character == "shopkeeper":
                if self.talking_phase == 1:
                    while True:
                        if self.skip_text and self.check_skip_cooldown <= 0:
                            self.check_skip_cooldown = 10
                            self.text += 1
                            self.skip_text = False
                        else:
                            self.check_skip_cooldown -= 1
                        if self.text == 0:
                            screen.blit(speech_block_img, (0, 480))
                            draw_text("?:", font, (255, 255, 255), 10, 490, 0.3)
                            draw_text("   Well would you look at that, there’s a new face around here. I haven\'t seen you before.", font, (255, 255, 255), 10, 510, 0.3)
                            draw_text("   Would you be interested in some extra, absolutely uncursed, items to help you on your journey?", font, (255, 255, 255), 10, 530, 0.3)
                        elif self.text == 1:
                            self.shop = True
                        break
        else:
            self.text = 0
            self.check_skip_cooldown = 10
            self.talking_phase = talking_phase
            self.shop = False

        return self.level_changer, self.talking_phase, self.shop

    def update(self):
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        self.vision.center = self.rect.center
        self.skip_text = skip_text

    def draw(self):
        screen.blit(self.image, self.rect)


class Shop():
    def __init__(self):
        self.max_health = player_max_health
        self.max_mana = player_max_mana
        self.wallet = wallet
        self.broke = False
        self.text_cooldown = 60

    def draw(self):
        if self.text_cooldown < 60:
            self.text_cooldown += 1
        else:
            self.broke = False
        if health_upgrade_btn.draw():
            if self.wallet >= 10:
                self.max_health += 1
                self.wallet -= 10
            else:
                self.broke = True
                self.text_cooldown = 0
        elif mana_upgrade_btn.draw():
            if self.wallet >= 10:
                self.max_mana += 1
                self.wallet -= 10
            else:
                self.broke = True
                self.text_cooldown = 0
        return self.max_health, self.max_mana, self.broke


class Boss(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, vision_height, vision_width, which_boss, phase):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        if which_boss == 1:
            self.health = 50
        elif which_boss == 2:
            self.health = 100
        elif which_boss == 3:
            self.health = 150
        elif which_boss == 4:
            self.health = 100
        self.speed = 4
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0
        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, vision_width, vision_height)
        self.idling = False
        self.idling_counter = 0
        self.boss = which_boss
        self.phase = phase
        if 1 <= self.boss <= 3:
            self.image = pygame.transform.scale(pygame.image.load(f'img/Enemy/Boss/World{self.boss}/0.png'), (318, 318))
        elif self.boss == 4:
            self.image = pygame.transform.scale(pygame.image.load(f'img/Enemy/Boss/World{self.phase}/0.png'),
                                                (318, 318))
        self.rect = self.image.get_rect()
        self.rect.center = (xcoords, ycoords)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_counter = 0
        self.ending = False

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
                self.health -= 10
            if pygame.sprite.spritecollide(self, arrow_group, True):
                self.health -= 1
            if not self.idling and random.randint(1, 200) == 1:
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

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 300
            n = random.randint(1, 3)
            if n == 1:
                for n in range(-3, 4):
                    fire_ball = FireAttack(self.rect.centerx + n * 250, self.rect.y - 200)
                    fire_attack_group.add(fire_ball)
            elif n == 2:
                ball = BallAttack(self.rect.centerx, self.rect.y, 1)
                ball_attack_group.add(ball)
                ball = BallAttack(self.rect.centerx, self.rect.y, -1)
                ball_attack_group.add(ball)
            elif n == 3:
                wall = WallAttack(self.rect.bottom)
                wall_attack_group.add(wall)
                wall = WallAttack(self.rect.bottom - wall_attack_img.get_height())
                wall_attack_group.add(wall)
                wall = WallAttack(self.rect.bottom - 2 * wall_attack_img.get_height())
                wall_attack_group.add(wall)

    def check_alive(self):
        if self.health <= 0:
            if self.boss == 1:
                self.health = 0
                self.speed = 0
                self.alive = False
                item = Item(self.rect.centerx, self.rect.centery, "Emerald")
                item_group.add(item)
            elif self.boss == 2:
                self.health = 0
                self.speed = 0
                self.alive = False
                item = Item(self.rect.centerx, self.rect.centery, "Ruby")
                item_group.add(item)
            elif self.boss == 3:
                self.health = 0
                self.speed = 0
                self.alive = False
                item = Item(self.rect.centerx, self.rect.centery, "Sapphire")
                item_group.add(item)
            elif self.boss == 4:
                self.health = 0
                self.speed = 0
                self.alive = False
                if self.phase < 3:
                    self.phase += 1
                    boss_group.empty()
                    boss = Boss(self.rect.centerx, self.rect.centery, 1500, 1000, 4, self.phase)
                    boss_group.add(boss)
                else:
                    self.ending = True
        return self.ending

    def update(self):
        self.attack_cooldown -= 1
        self.check_alive()
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        if not self.alive:
            self.kill()

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
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
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
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 4:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", 1)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
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
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 8:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", -1)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 9:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", -1)
                        exit_group.add(exit_sign)

                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 10:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", -1)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 11:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", -4)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 12:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", 4)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 13:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", 5)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 14:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", -5)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 15:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", 7)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 16:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", -7)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 17:
                        exit_sign = Exit(exitup_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Down", -13)
                        exit_group.add(exit_sign)
                        if previous_level == "Up":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 18:
                        exit_sign = Exit(exitdown_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Up", 13)
                        exit_group.add(exit_sign)
                        if previous_level == "Down":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
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
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
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
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
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
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 25:
                        exit_sign = Exit(exitright_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Left", -4)
                        exit_group.add(exit_sign)
                        if previous_level == "Right":
                            player_character = Player((xcoords + 0.5 * player.direction) * tile_size + self.hor_off,
                                                      ycoords * tile_size + self.ver_off)
                    elif one_tile == 26:
                        exit_sign = Exit(exitleft_img, xcoords * tile_size + self.hor_off,
                                         ycoords * tile_size + self.ver_off, "Right", 4)
                        exit_group.add(exit_sign)
                        if previous_level == "Left":
                            player_character = Player((xcoords + 0.5 + player.direction) * tile_size + self.hor_off,
                                                     (ycoords + 0.5) * tile_size + self.ver_off)
                    elif one_tile == 27:
                        one_enemy = Enemy(False, xcoords * tile_size + self.hor_off,
                                          ycoords * tile_size + self.ver_off, 2, 300, 600)
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
                    elif one_tile == 35:
                        npc = Npc(xcoords * tile_size + self.hor_off, ycoords * tile_size + self.ver_off, 'portalman')
                        npc_group.add(npc)
                    elif one_tile == 36:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 37:
                        npc = Npc(xcoords * tile_size + self.hor_off, ycoords * tile_size + self.ver_off, 'shopkeeper')
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
                                                      (ycoords + 0.5) * tile_size + self.ver_off)
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
                    elif one_tile == 44:
                        one_boss = Boss(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, 1500, 1000, 1, 1)
                        boss_group.add(one_boss)
                    elif one_tile == 45:
                        one_boss = Boss(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, 1500, 1000, 2, 1)
                        boss_group.add(one_boss)
                    elif one_tile == 46:
                        one_boss = Boss(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, 1500, 1000, 3, 1)
                        boss_group.add(one_boss)
                    elif one_tile == 47:
                        one_boss = Boss(xcoords * tile_size + self.hor_off,
                                        ycoords * tile_size + self.ver_off, 1500, 1000, 4, 1)
                        boss_group.add(one_boss)
                    elif one_tile == 48:
                        one_enemy = Enemy(True, xcoords * tile_size + self.hor_off,
                                          ycoords * tile_size + self.ver_off, 1, 300, 600)
                        enemy_group.add(one_enemy)
                    elif one_tile == 49:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 50:
                        self.obstacle_list.append(tile_data)
                    elif one_tile == 51:
                        self.obstacle_list.append(tile_data)
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
                player.health += 1
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Mana":
                player.mana += 1
                if player.health > player.max_mana:
                    player.health = player.max_mana
            elif self.item_type == "Money":
                player.wallet += 1
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
            self.kill()
        return [self.walljump_acquired, self.doublejump_acquired, self.emerald_acquired,
                self.ruby_acquired, self.sapphire_acquired]


class Arrow(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 14
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
        self.speed = 10
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


class Slime(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, direction, world):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        if world == 0:
            self.image = slimeball_img
        elif world == 1:
            self.image = desert_slimeball_img
        elif world == 2:
            self.image = lava_slimeball_img
        elif world == 3:
            self.image = snow_slimeball_img
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


class FireAttack(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords):
        pygame.sprite.Sprite.__init__(self)
        self.image = fire_attack_img
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.center = (xcoords, ycoords)
        self.lifetime = 500
        self.vel_y = 0

    def update(self):
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect.x, self.rect.y + self.vel_y, self.width, self.height):
                self.vel_y = one_tile[1].top - self.rect.bottom
        self.rect.y += self.vel_y
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class BallAttack(pygame.sprite.Sprite):
    def __init__(self, xcoords, ycoords, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_attack_img
        self.direction = direction
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.center = (xcoords, ycoords)
        self.lifetime = 1000
        self.vel_y = 0
        self.speed = 4

    def update(self):
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
        for one_tile in world.obstacle_list:
            if one_tile[1].colliderect(self.rect.x + self.speed * self.direction, self.rect.y, self.width, self.height):
                self.direction *= -1
            if one_tile[1].colliderect(self.rect.x, self.rect.y + self.vel_y, self.width, self.height):
                self.vel_y *= -0.9
        self.rect.x += self.speed * self.direction
        self.rect.y += self.vel_y
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class WallAttack(pygame.sprite.Sprite):
    def __init__(self, ycoords):
        pygame.sprite.Sprite.__init__(self)
        self.image = wall_attack_img
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        n = random.randint(1, 2)
        if n == 1:
            self.rect.center = (0, ycoords)
            self.direction = 1
        elif n == 2:
            self.rect.center = ((cols - 1) * tile_size, ycoords)
            self.direction = -1
        self.lifetime = 1000
        self.vel_y = 0
        self.speed = 4

    def update(self):
        self.rect.x += self.speed * self.direction
        self.rect.x += int(scroll_hor)
        self.rect.y += int(scroll_ver)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class Ending:
    def __init__(self):
        self.cooldown = 0

    def update(self):
        self.cooldown += 1
        if self.cooldown <= 120:
            screen.fill((0, 0, 0))
            draw_text("Phew.. thank god that’s over with.", font, (255, 255, 255), 0.4 * screen_width, screen_height // 2, 0.5)
        elif 120 < self.cooldown <= 240:
            screen.blit(ending0_img, (0, 0))
        elif 240 < self.cooldown <= 360:
            screen.fill((0, 0, 0))
            draw_text("Just a few more steps.", font, (255, 255, 255), 0.4 * screen_width,
                      screen_height // 2, 0.5)
        elif 360 < self.cooldown <= 480:
            screen.blit(ending1_img, (0, 0))
        elif 480 < self.cooldown <= 600:
            screen.fill((0, 0, 0))
            draw_text("I better get to the portal before he respawns or something..", font, (255, 255, 255), 0.1 * screen_width,
                      screen_height // 2, 0.5)
        elif 600 < self.cooldown <= 720:
            screen.blit(ending2_img, (0, 0))
        elif 720 < self.cooldown <= 840:
            screen.fill((0, 0, 0))
            draw_text("It’s time to go back home.", font, (255, 255, 255), 0.4 * screen_width,
                      screen_height // 2, 0.5)
        elif 840 < self.cooldown <= 960:
            screen.blit(ending3_img, (0, 0))
        elif 960 < self.cooldown <= 1080:
            screen.fill((0, 0, 0))
            draw_text("..Huh? Why am I back here?", font, (255, 255, 255), 0.4 * screen_width,
                      screen_height // 2, 0.5)
        elif 1080 < self.cooldown <= 1200:
            screen.blit(ending4_img, (0, 0))
        elif 1200 < self.cooldown <= 2000:
            screen.blit(ending5_img, (0, 0))


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
slime_group = pygame.sprite.Group()
fire_attack_group = pygame.sprite.Group()
ball_attack_group = pygame.sprite.Group()
wall_attack_group = pygame.sprite.Group()

shop_menu = Shop()

start_btn = Button((screen_width - start_img.get_width()) // 2, screen_height // 1 - 200, start_img)
exit_btn = Button((screen_width - exit_img.get_width()) // 2, screen_height // 1 - 150, exit_img)
respawn_btn = Button((screen_width - respawn_img.get_width()) // 2, screen_height // 1 - 200, respawn_img)
settings_btn = Button((screen_width - settings_img.get_width()) // 2, screen_height // 1 - 250, settings_img)
volume_up_btn = Button((screen_width - volume_up_img.get_width()) // 2 + 100, screen_height // 1 - 200, volume_up_img)
volume_down_btn = Button((screen_width - volume_down_img.get_width()) // 2 - 100, screen_height // 1 - 200, volume_down_img)
inventory_btn = Button((screen_width - inventory_btn_img.get_width()) // 2, screen_height // 1 - 300, inventory_btn_img)
save_btn = Button((screen_width - save_img.get_width()) // 2, screen_height // 1 - 400, save_img)
load_btn = Button((screen_width - load_img.get_width()) // 2, screen_height // 1 - 350, load_img)
mana_upgrade_btn = Button((screen_width - mana_img.get_width()) // 2, screen_height // 1 - 350, mana_img)
health_upgrade_btn = Button((screen_width - health_img.get_width()) // 2, screen_height // 1 - 500, health_img)
ending_screen = Ending()

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
        if level == 0 and not music_started:
            play_music(0)
            music_started = True
        draw_bg()
        world.draw()
        for x in range(player_max_health):
            screen.blit(max_health_img, (90 + (x * 20), 40))
        for x in range(player.health):
            screen.blit(health_img, (90 + (x * 20), 40))
        for x in range(player_max_mana):
            screen.blit(max_mana_img, (90 + (x * 20), 60))
        for x in range(player.mana):
            screen.blit(mana_img, (90 + (x * 20), 60))
        screen.blit(money_img, (90, 85))
        draw_text(f"{player.wallet}", font, (255, 255, 0), 115, 85, 0.35)

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()
            for x in range(enemy.health):
                screen.blit(pygame.transform.scale(pygame.image.load("img/menu/HP bar.png"), (2, 2)), (enemy.rect.centerx + (2 * x) - 20, enemy.rect.centery - 30))
        for boss in boss_group:
            boss.ai()
            boss.update()
            boss.draw()
            for x in range(boss.health):
                screen.blit(pygame.image.load("img/menu/HP bar.png"), (300 + (4 * x), 100))

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
        slime_group.update()
        fire_attack_group.update()
        ball_attack_group.update()
        wall_attack_group.update()
        arrow_group.draw(screen)
        spell_group.draw(screen)
        item_group.draw(screen)
        decoration_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        npc_group.draw(screen)
        slime_group.draw(screen)
        fire_attack_group.draw(screen)
        ball_attack_group.draw(screen)
        wall_attack_group.draw(screen)

        scroll_hor, scroll_ver, level_change, previous_level_number = player.move(moving_left, moving_right)
        if previous_level_number != 0:
            previous_level = previous_level_number
        total_hor_scroll -= scroll_hor
        total_ver_scroll -= scroll_ver
        if player.alive:
            player.update()
            player.draw()
            while True:
                if cast:
                    player.cast()
                    player.update_action(4)
                    break
                if shoot:
                    player.shoot()
                    player.update_action(3)
                    break
                if attack:
                    player.melee()
                if player.attacking:
                    player.update_action(7)
                    break
                if player.touching_wall and player.in_air:
                    player.update_action(6)
                    break
                if player.in_air:
                    player.update_action(2)
                    break
                if moving_left or moving_right:
                    player.update_action(1)
                    shop = False
                    break
                else:
                    player.update_action(0)
                    break

            if map_menu:
                screen.blit(map_background_img, (0, 0))
                screen.blit(map_img, (0, 0))
                screen.blit(pygame.transform.scale(pygame.image.load("img/menu/HP bar.png"), (10, 10)), pos_dict[level])

            if controls:
                screen.blit(controls_img, (screen_width - controls_img.get_width(), inventory_img.get_height()))
            else:
                draw_text("For Controls Press TAB", font, (255, 255, 255), 880, 126, 0.2)
                draw_text("When Glitched Press Delete", font, (255, 255, 255), 866, 140, 0.2)
                draw_text("Press SPACE To Skip Text", font, (255, 255, 255), 870, 154, 0.2)

            if level_change == 0:
                for npc in npc_group:
                    level_change, talking_phase, shop = npc.interact()
                    npc.update()
                if moving_left or moving_right:
                    shop = False

            for boss in boss_group:
                if boss.check_alive():
                    ending = True
            if ending:
                music_index = play_music(50)
                ending_screen.update()

            if shop:
                player_max_health, player_max_mana, broke = shop_menu.draw()
                if broke:
                    screen.blit(speech_block_img, (0, 480))
                    draw_text("   You don\'t have enough money", font, (255, 255, 255), 10,
                              510, 0.3)

            if pause_menu:
                screen.fill((0, 0, 0))
                if settings:
                    if volume_up_btn.draw():
                        if volume < 10:
                            volume += 1
                    elif volume_down_btn.draw():
                        if volume > 0:
                            volume -= 1
                elif inventory:
                    screen.blit(inventory_img, (screen_width - inventory_img.get_width(), 0))
                    if emerald_acquired:
                        screen.blit(pygame.transform.scale(emerald_img, (28, 28)), (884, 14))
                    if ruby_acquired:
                        screen.blit(pygame.transform.scale(ruby_img, (28, 28)), (884, 47))
                    if sapphire_acquired:
                        screen.blit(pygame.transform.scale(sapphire_img, (18, 28)), (889, 80))
                    if doublejump_acquired:
                        screen.blit(pygame.transform.scale(double_jump_item, (28, 28)), (916, 14))
                    if walljump_acquired:
                        screen.blit(pygame.transform.scale(wall_jump_item, (28, 28)), (916, 47))
                else:
                    if exit_btn.draw():
                        run = False
                    elif respawn_btn.draw():
                        player.health = 0
                        pause_menu = False
                    elif settings_btn.draw():
                        settings = True
                    elif inventory_btn.draw():
                        inventory = True
                    elif load_btn.draw():
                        with open("savefile.txt", "r") as f:
                            list = []
                            for item in f.readlines():
                                list.append(item.strip("\n"))
                            player_max_mana, player_max_health, player_mana, player_health, previous_level, level, wallet, gathered_item_list, walljump_acquired, doublejump_acquired, emerald_acquired, ruby_acquired, sapphire_acquired = list
                        print(walljump_acquired, doublejump_acquired, emerald_acquired, ruby_acquired, sapphire_acquired)
                        player_max_mana = int(player_max_mana)
                        player_max_health = int(player_max_health)
                        player_mana = int(player_mana)
                        player_health = int(player_health)
                        level = int(level)
                        wallet = int(wallet)
                        total_hor_scroll = 0
                        total_ver_scroll = 0
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
                        world_data = reset_level()
                        player = None
                        with open(f'level_data/level_data{level}.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)
                        total_hor_scroll = -world.hor_off
                        total_ver_scroll = -world.ver_off
                        music_index = play_music(level)
                        fade(screen)
                        pause_menu = False
                    elif save_btn.draw():
                        with open("savefile.txt", "w") as f:
                            f.write(f"{player_max_mana}\n"
                                    f"{player_max_health}\n"
                                    f"{player_mana}\n"
                                    f"{player_health}\n"
                                    f"{previous_level}\n"
                                    f"{level}\n"
                                    f"{wallet}\n"
                                    f"{gathered_item_list}\n"
                                    f"{walljump_acquired}\n"
                                    f"{doublejump_acquired}\n"
                                    f"{emerald_acquired}\n"
                                    f"{ruby_acquired}\n"
                                    f"{sapphire_acquired}")

            if level_change != 0:
                total_hor_scroll = 0
                total_ver_scroll = 0
                level += level_change
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
                level_change = 0
                player_health = player.health
                player_mana = player.mana
                wallet = player.wallet
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
                music_index = play_music(level)
                fade(screen)

        else:
            scroll_ver = 0
            scroll_hor = 0
            screen.blit(game_over_img, (0, 0))
            if respawn_btn.draw():
                player_health = player_max_health
                wallet = player.wallet
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
                fade(screen)
                pause_menu = False
            elif exit_btn.draw():
                run = False
    else:
        screen.blit(title_img, (0, 0))
        if start_btn.draw():
            game_started = True
        if exit_btn.draw():
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_z and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                if pause_menu and not (settings or inventory):
                    pause_menu = False
                elif settings:
                    settings = False
                elif inventory:
                    inventory = False
                else:
                    pause_menu = True
            if event.key == pygame.K_a:
                shoot = True
            if event.key == pygame.K_s:
                cast = True
            if event.key == pygame.K_m:
                if map_menu:
                    map_menu = False
                else:
                    map_menu = True
            if event.key == pygame.K_DELETE:
                player.alive = False
            if event.key == pygame.K_x:
                attack = True
            if event.key == pygame.K_i:
                inventory = True
            if event.key == pygame.K_TAB:
                controls = True
            if event.key == pygame.K_SPACE:
                skip_text = True

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
            if event.key == pygame.K_x:
                attack = False
            if event.key == pygame.K_i:
                inventory = False
            if event.key == pygame.K_TAB:
                controls = False
            if event.key == pygame.K_SPACE:
                skip_text = False
    print(gathered_item_list)
    clock.tick(fps)
    pygame.display.update()

pygame.quit()
