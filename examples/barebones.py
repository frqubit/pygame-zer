import pygame
import pyzer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pyzer.PygameDriver(screen)

pyzer.Circle(zerdriver, (100, 100), 25, fill="red")
pyzer.Circle(zerdriver, (200, 250), 15, fill="green")
pyzer.Circle(zerdriver, (200, 275), 15, fill="green", outline="red", outlineWidth=2)
pyzer.Rect(zerdriver, (300, 350, 15, 35))
pyzer.Rect(zerdriver, (550, 600, 75, 50), outline="blue")
pyzer.Line(zerdriver, (500, 400), (200, 780))

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
