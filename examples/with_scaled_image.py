import pygame

import pygame_zer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pygame_zer.PygameDriver(screen)

# https://commons.wikimedia.org/wiki/File:Anas_platyrhynchos_(mixed_pair)_(32428014687).jpg
image = pygame.image.load("examples/ducks.jpg")

pygame_zer.Rect(zerdriver, (0, 0, 500, 500), outlineWidth=0)
pygame_zer.Image(zerdriver, image, (100, 100), (200, 200))
pygame_zer.Image(zerdriver, image, (300, 300), (1000, 1000))
pygame_zer.Circle(zerdriver, (300, 300), 50, fill="red")


running = True
while running:
    for event in pygame.event.get():
        if zerdriver.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    zerdriver.draw()
    # zerdriver.camera.topleft = (220, 220)

    pygame.display.flip()

pygame.quit()
