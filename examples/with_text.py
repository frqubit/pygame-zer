import pygame
import pygame.freetype
import pyzer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pyzer.PygameDriver(screen, flags=pyzer.F_DEFAULT | pyzer.F_NOCACHE)

font = pygame.freetype.SysFont("Arial", 20)

pyzer.Text(zerdriver, (100, 100), font, "Hello!")

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
