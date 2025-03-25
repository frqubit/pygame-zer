import pygame
import pyzer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pyzer.PygameDriver(screen)

circle = pyzer.Circle(zerdriver, (100, 100), 25, fill="red")

running = True
velocity = 5
ticks_left = 120
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if zerdriver.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    zerdriver.draw(screen)

    circle.translate(velocity, 0)
    if ticks_left == 0:
        if velocity > 0:
            circle.fill = "red"
        else:
            circle.fill = "green"
        velocity *= -1
        ticks_left = 121

    pygame.display.flip()
    clock.tick(60)
    ticks_left -= 1

pygame.quit()
