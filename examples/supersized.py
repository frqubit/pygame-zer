import pygame

import pygame_zer

pygame.init()

screen = pygame.display.set_mode((1024, 720))
driver = pygame_zer.Driver(screen, flags=pygame_zer.DriverFlags.ZOOMABLE)
display_font = pygame.font.SysFont("Arial", 10)

driver.camera.minzoom = 1e-15
driver.camera.maxzoom = 1e25

pygame_zer.Circle(driver, (512, 360), 1)
image = pygame.image.load("examples/ducks.jpg")
pygame_zer.Image(driver, image, (1e10, 5e9), (5e9, 5e9))
pygame_zer.Rect(driver, (512 - 1e-5, 360 - 1e-5, 2e-5, 2e-5), "red")

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
