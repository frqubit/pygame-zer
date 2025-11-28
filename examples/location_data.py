import pygame

import pygame_zer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
driver = pygame_zer.Driver(screen)

display_font = pygame.font.SysFont("Arial", 10)

pygame_zer.Rect(driver, (50, 50, 100, 100))
pygame_zer.Circle(driver, (100, 100), 25, fill="red")

running = True
while running:
    for event in pygame.event.get():
        if driver.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))
    driver.draw()

    location = display_font.render(str(driver.camera.topleft), False, "white")
    zoom = display_font.render(str(driver.camera.camerazoom), False, "white")

    screen.blit(location, (10, 10))
    screen.blit(zoom, (10, 25))

    pygame.display.flip()

pygame.quit()
