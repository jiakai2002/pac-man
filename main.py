import math
import sys

import pygame

from board import boards

pygame.init()
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Pac-Man")
font = pygame.font.Font("assets/fonts/PublicPixel-z84yD.ttf", 17)
n1 = (HEIGHT - 50) // 32  # vertical space of each block
n2 = WIDTH // 30  # horizontal space of each block
level = boards  # add more boards in future
color = "blue"
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(
        pygame.transform.scale(
            pygame.image.load(f"assets/player_images/{i}.png"), (45, 45)
        )
    )
blinky_image = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/red.png"), (45, 45)
)
pinky_image = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/pink.png"), (45, 45)
)
inky_image = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/blue.png"), (45, 45)
)
clyde_image = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/orange.png"), (45, 45)
)
spooked_image = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/powerup.png"), (45, 45)
)
dead_image = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/dead.png"), (45, 45)
)
player_x = 450
player_y = 663

blink_x = 56
blinky_y = 58
blinky_direction = 0

inky_x = 440
ink = 338
inky_direction = 2

pinky_x = 440
pinky_y = 438
pinky_direction = 2


clyde_x = 440
clyde_y = 438
clyde_direction = 2

blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False

blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False

ghost_speed = 2

direction = 0
direction_command = 0
count = 0
flicker = False
turns_allowed = [False, False, False, False]
player_speed = 2
score = 0
powerup = False
power_counter = 0
startup_counter = 0
moving = False
lives = 3

eaten_ghosts = [False, False, False, False]
targets = [
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
]


def draw_misc():
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (20, 920))
    if powerup:
        pygame.draw.circle(screen, color, (250, 930), 14)
    for i in range(lives):
        screen.blit(
            pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915)
        )


def check_collisions(score, powerup, power_count, eaten_ghosts):
    if 0 < player_x < 870:
        if level[center_y // n1][center_x // n2] == 1:
            level[center_y // n1][center_x // n2] = 0
            score += 10
        if level[center_y // n1][center_x // n2] == 2:
            level[center_y // n1][center_x // n2] = 0
            score += 50
            powerup = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return score, powerup, power_count, eaten_ghosts


def draw_board(level):
    rows = len(level)
    cols = len(level[0])
    for i in range(rows):
        for j in range(cols):
            if level[i][j] == 1:
                pygame.draw.circle(
                    screen, "white", (j * n2 + (0.5 * n2), i * n1 + (0.5 * n1)), 4
                )
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(
                    screen, "white", (j * n2 + (0.5 * n2), i * n1 + (0.5 * n1)), 10
                )
            if level[i][j] == 3:
                pygame.draw.line(
                    screen,
                    color,
                    (j * n2 + (0.5 * n2), i * n1),
                    (j * n2 + (0.5 * n2), i * n1 + n1),
                    3,
                )
            if level[i][j] == 4:
                pygame.draw.line(
                    screen,
                    color,
                    (j * n2, i * n1 + 0.5 * n1),
                    (j * n2 + n2, i * n1 + 0.5 * n1),
                    3,
                )
            if level[i][j] == 5:
                pygame.draw.arc(
                    screen,
                    color,
                    [j * n2 - 0.4 * n2 - 2, i * n1 + 0.5 * n1, n2, n1],
                    0,
                    PI / 2,
                    3,
                )
            if level[i][j] == 6:
                pygame.draw.arc(
                    screen,
                    color,
                    [j * n2 + 0.5 * n2, i * n1 + 0.5 * n1, n2, n1],
                    PI / 2,
                    PI,
                    3,
                )
            if level[i][j] == 7:
                pygame.draw.arc(
                    screen,
                    color,
                    [j * n2 + 0.5 * n2, i * n1 - 0.4 * n1, n2, n1],
                    PI,
                    3 * PI / 2,
                    3,
                )
            if level[i][j] == 8:
                pygame.draw.arc(
                    screen,
                    color,
                    [j * n2 - 0.4 * n2 - 2, i * n1 - 0.4 * n1, n2, n1],
                    3 * PI / 2,
                    2 * PI,
                    3,
                )
            if level[i][j] == 9:
                pygame.draw.line(
                    screen,
                    "white",
                    (j * n2, i * n1 + 0.5 * n1),
                    (j * n2 + n2, i * n1 + 0.5 * n1),
                    3,
                )


def draw_player():
    if direction == 0:
        screen.blit(player_images[count // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(
            pygame.transform.flip(player_images[count // 5], True, False),
            (player_x, player_y),
        )
    elif direction == 2:
        screen.blit(
            pygame.transform.rotate(player_images[count // 5], 90),
            (player_x, player_y),
        )
    elif direction == 3:
        screen.blit(
            pygame.transform.rotate(player_images[count // 5], 270),
            (player_x, player_y),
        )


def check_position(center_x, center_y):
    turns = [False, False, False, False]
    fudge = 15
    # check collisions based on center x and center y +/- fudge number
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // n1][(center_x - fudge) // n2] < 3:
                turns[1] = True
        if direction == 1:
            if level[center_y // n1][(center_x + fudge) // n2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(center_y + fudge) // n1][(center_x // n2)] < 3:
                turns[3] = True
        if direction == 3:
            if level[(center_y - fudge) // n1][center_x // n2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= center_x % n2 <= 18:
                if level[(center_y + fudge) // n1][center_x // n2] < 3:
                    turns[3] = True
                if level[(center_y - fudge) // n1][center_x // n2] < 3:
                    turns[2] = True
            if 12 <= center_y % n1 <= 18:
                if level[center_y // n1][(center_x - n2) // n2] < 3:
                    turns[1] = True
                if level[center_y // n1][(center_x + n2) // n2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= center_x % n2 <= 18:
                if level[(center_y + n1) // n1][center_x // n2] < 3:
                    turns[3] = True
                if level[(center_y - n1) // n1][center_x // n2] < 3:
                    turns[2] = True
            if 12 <= center_y % n1 <= 18:
                if level[center_y // n1][(center_x - fudge) // n2] < 3:
                    turns[1] = True
                if level[center_y // n1][(center_x + fudge) // n2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns


def move_player(player_x, player_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        player_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        player_x -= player_speed
    elif direction == 2 and turns_allowed[2]:
        player_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        player_y += player_speed
    return player_x, player_y


run = True
while run:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                direction_command = 0
            if event.key == pygame.K_a:
                direction_command = 1
            if event.key == pygame.K_w:
                direction_command = 2
            if event.key == pygame.K_s:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_a and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_w and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_s and direction_command == 3:
                direction_command = direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    # timers
    if count < 19:
        count += 1
        if count > 3:
            flicker = False
    else:
        count = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True

    draw_board(level)
    draw_player()
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    score, powerup, power_counter, eaten_ghosts = check_collisions(
        score, powerup, power_counter, eaten_ghosts
    )
    draw_misc()

    pygame.display.update()
    clock.tick(60)
