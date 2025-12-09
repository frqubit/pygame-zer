import pygame

import pygame_zer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pygame_zer.PygameDriver(screen)

circle = pygame_zer.Circle(zerdriver, (100, 100), 25, fill="red")

running = True
while running:
    for event in pygame.event.get():
        if zerdriver.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    mouse_pos = pygame.mouse.get_pos()
    if circle.hitbox.contains_point(zerdriver.camera.point_to_world(mouse_pos)):
        circle.fill = "green"
    else:
        circle.fill = "red"

    zerdriver.draw()

    pygame.display.flip()

pygame.quit()
