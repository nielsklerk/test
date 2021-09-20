import pygame
import os
import csv

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1024
screen_height = 576
tile_size = 64
game_over = False

gravity = 0.7

moving_left = False
moving_right = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PWS")


def draw_bg():
    screen.fill((100, 100, 100))
    pygame.draw.line(screen, (255, 0, 0), (0, 500), (screen_width, 500))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.in_air = True
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(5):
            img = pygame.image.load("img/New Piskel.png")
            img = pygame.transform.scale(img, (50, 100))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load("img/New Piskel.png")
            img = pygame.transform.scale(img, (50, 100))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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

    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Player(100, 500, 5)

run = True
while run:
    clock.tick(fps)

    draw_bg()
    player.draw()

    if player.alive:
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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
