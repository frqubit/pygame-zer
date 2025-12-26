import pygame

import pygame_zer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pygame_zer.PygameDriver(screen)

red = pygame_zer.Circle(zerdriver, (100, 100), 25, fill="red")
green = pygame_zer.Circle(zerdriver, (500, 500), 25, fill="green")


def print_color(color):
    def wrapper():
        print(color)

    return wrapper


red.onclick = print_color("red")
green.onclick = print_color("green")

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
