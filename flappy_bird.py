import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     
        screen.fill((0, 255, 0))           
    # pygame.draw.rect(
    # screen,
    # (255,0,0),
    # (800,100,50,80)
# )

    pygame.display.flip()


pygame.quit()
