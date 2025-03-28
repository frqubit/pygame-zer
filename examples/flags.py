import pygame
import pygame_zer
import sys

arg1 = sys.argv[1] if len(sys.argv) > 1 else ["", ""]
flags = pygame_zer.F_EMPTY
if 'z' in arg1:
    flags = flags | pygame_zer.F_ZOOMABLE
if 'e' in arg1:
    flags = flags | pygame_zer.F_EXPLORABLE

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pygame_zer.PygameDriver(screen, flags=flags)

# https://commons.wikimedia.org/wiki/File:Anas_platyrhynchos_(mixed_pair)_(32428014687).jpg
image = pygame.image.load("examples/ducks.jpg")

pygame_zer.Image(zerdriver, image, (200, 200))

running = True
while running:
    for event in pygame.event.get():
        if zerdriver.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    zerdriver.draw()

    pygame.display.flip()

pygame.quit()
