import pygame
import pygame.freetype

import pygame_zer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pygame_zer.PygameDriver(screen, flags=pygame_zer.DriverFlags.NOCACHE)

font = pygame.freetype.SysFont("Arial", 20)

pygame_zer.Text(zerdriver, (100, 100), font, "Hello!")

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
