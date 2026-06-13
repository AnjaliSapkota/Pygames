import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

# Colors
SKY        = (113, 197, 207)
GROUND_COL = ( 78, 174,  93)
DIRT_COL   = (218, 176, 120)
PIPE_COL   = ( 84, 175,  82)
PIPE_DARK  = ( 56, 135,  56)
BIRD_BODY  = (255, 215,   0)
BIRD_WING  = (255, 165,   0)
BIRD_EYE   = (255, 255, 255)
BIRD_PUPIL = ( 30,  30,  30)
BIRD_BEAK  = (255, 130,   0)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
SHADOW     = (  0,   0,   0,  80)

#  Constants
GRAVITY = 0.4
FLAP = -7

PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_WIDTH = 60

BIRD_X = 80
BIRD_R = 18

GROUND_HEIGHT = 60

score_font = pygame.font.SysFont("comicsansms", 48)
game_font = pygame.font.SysFont("comicsansms", 28)


# Cloud Class
class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(0.3, 1)

    def update(self):
        self.x -= self.speed

        if self.x < -80:
            self.x = WIDTH + random.randint(50, 150)
            self.y = random.randint(20, HEIGHT // 2)

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, (self.x, self.y, 60, 30))
        pygame.draw.ellipse(surface, WHITE, (self.x + 15, self.y - 10, 40, 25))
        pygame.draw.ellipse(surface, WHITE, (self.x + 30, self.y, 35, 20))


clouds = [
    Cloud(
        random.randint(0, WIDTH),
        random.randint(20, HEIGHT // 2)
    )
    for _ in range(5)
]


# Bird Drawing
def draw_bird(surface, x, y):

    pygame.draw.circle(
        surface,
        BIRD_BODY,
        (x, int(y)),
        BIRD_R
    )

    pygame.draw.circle(
        surface,
        BIRD_WING,
        (x - 5, int(y)),
        8
    )

    pygame.draw.circle(
        surface,
        BIRD_EYE,
        (x + 6, int(y) - 6),
        4
    )

    pygame.draw.circle(
        surface,
        BIRD_PUPIL,
        (x + 7, int(y) - 6),
        2
    )

    pygame.draw.polygon(
        surface,
        BIRD_BEAK,
        [
            (x + 15, y),
            (x + 25, y + 3),
            (x + 15, y + 6)
        ]
    )


# Pipes
pipes = []


def spawn_pipe():

    top = random.randint(
        80,
        HEIGHT - GROUND_HEIGHT - PIPE_GAP - 80
    )

    pipes.append([WIDTH, top, False])


# Reset Game
def reset():

    global bird_y
    global bird_vel
    global pipes
    global score
    global alive

    bird_y = HEIGHT // 2
    bird_vel = 0

    pipes = []

    score = 0
    alive = True

    spawn_pipe()


# Collision
def check_collision():

    for px, top, _ in pipes:

        if (
            BIRD_X + BIRD_R > px
            and BIRD_X - BIRD_R < px + PIPE_WIDTH
        ):

            if (
                bird_y - BIRD_R < top
                or bird_y + BIRD_R > top + PIPE_GAP
            ):
                return True

    if bird_y + BIRD_R >= HEIGHT - GROUND_HEIGHT:
        return True

    if bird_y - BIRD_R <= 0:
        return True

    return False



# Start Game
reset()

running = True

# Main Loop
while running:

    clock.tick(60)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if alive:
                    bird_vel = FLAP
                else:
                    reset()

    # Update
    if alive:

        bird_vel += GRAVITY
        bird_y += bird_vel

        # Clouds
        for cloud in clouds:
            cloud.update()

        # Pipes
        for pipe in pipes:
            pipe[0] -= PIPE_SPEED

        pipes = [
            pipe
            for pipe in pipes
            if pipe[0] > -PIPE_WIDTH
        ]

        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 220:
            spawn_pipe()

        # Score
        for pipe in pipes:

            if (
                not pipe[2]
                and pipe[0] + PIPE_WIDTH < BIRD_X
            ):
                pipe[2] = True
                score += 1

        if check_collision():
            alive = False

    # Draw
    screen.fill(SKY)

    # Clouds
    for cloud in clouds:
        cloud.draw(screen)

    # Pipes
    for px, top, _ in pipes:

        pygame.draw.rect(
            screen,
            PIPE_COL,
            (px, 0, PIPE_WIDTH, top)
        )

        pygame.draw.rect(
            screen,
            PIPE_DARK,
            (px, 0, PIPE_WIDTH, top),
            3
        )

        pygame.draw.rect(
            screen,
            PIPE_COL,
            (
                px,
                top + PIPE_GAP,
                PIPE_WIDTH,
                HEIGHT
            )
        )

        pygame.draw.rect(
            screen,
            PIPE_DARK,
            (
                px,
                top + PIPE_GAP,
                PIPE_WIDTH,
                HEIGHT
            ),
            3
        )

    # Ground
    pygame.draw.rect(
        screen,
        GROUND_COL,
        (
            0,
            HEIGHT - GROUND_HEIGHT,
            WIDTH,
            GROUND_HEIGHT
        )
    )

    # Bird
    draw_bird(screen, BIRD_X, bird_y)

    # Score
    score_text = score_font.render(
        str(score),
        True,
        BLACK
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 - score_text.get_width() // 2,
            20
        )
    )

    # Game Over
    if not alive:

        over_text = game_font.render(
            "GAME OVER",
            True,
            BLACK
        )

        restart_text = game_font.render(
            "Press SPACE to restart",
            True,
            BLACK
        )

        screen.blit(
            over_text,
            (
                WIDTH // 2 - over_text.get_width() // 2,
                HEIGHT // 2 - 30
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                HEIGHT // 2 + 10
            )
        )

    pygame.display.flip()