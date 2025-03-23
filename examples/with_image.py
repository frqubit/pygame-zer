import pygame
import pyzer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pyzer.PygameDriver(screen)

# https://commons.wikimedia.org/wiki/File:Anas_platyrhynchos_(mixed_pair)_(32428014687).jpg
image = pygame.image.load("examples/ducks.jpg")

pyzer.Image(zerdriver, image, (200, 200))

running = True
while running:
    for event in pygame.event.get():
        if zerdriver.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    zerdriver.draw(screen)

    pygame.display.flip()

pygame.quit()
