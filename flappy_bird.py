import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

# Colors
BLUE = (135, 206, 235)
YELLOW = (255, 200, 0)

# Bird settings
BIRD_R = 20


def draw_bird(surface, x, y):
    pygame.draw.circle(surface, YELLOW, (x, y), BIRD_R)


x = 50
y = 250
velocity = 0

# x = 0


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = -6   


    velocity += 0.3   # gravity
    y += velocity

    
    screen.fill(BLUE)

    # DRAW
    draw_bird(screen, x, int(y))

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
