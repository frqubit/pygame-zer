import math

import pygame

import pygame_zer
from pygame_zer.types import f, vec2f

pygame.init()
screen = pygame.display.set_mode((800, 600))
driver = pygame_zer.Driver(screen, pygame_zer.DriverFlags.empty())
display_font = pygame.font.SysFont("Arial", 10)
driver.camera.topleft = vec2f(-400, -300)

driver.camera.set_zoom_limits(1e15, 1e25)
driver.zoom_sensitivity = f(1.5)

pygame_zer.Circle(driver, (512, 360), 1)
image = pygame.image.load("examples/ducks.jpg")
pygame_zer.Image(driver, image, (1e10, 5e9), (5e9, 5e9))
pygame_zer.Rect(driver, (0 - 1e-5, 0 - 1e-5, 2e-5, 2e-5), "red")
slider_x = 400


def mouse_touching_slider():
    global slider_x
    mouse_x, mouse_y = pygame.mouse.get_pos()
    slider_y = 537.5
    distance = math.sqrt((mouse_x - slider_x) ** 2 + (mouse_y - slider_y) ** 2)
    return distance < 30


def set_camera_to_zoom_by_ratio(ratio):
    min_zoom = driver.camera.minzoom
    max_zoom = driver.camera.maxzoom

    min_zoom_log = math.log(min_zoom)
    max_zoom_log = math.log(max_zoom)

    new_zoom = math.e ** ((max_zoom_log - min_zoom_log) * ratio + min_zoom_log)
    driver.camera.camerazoom = f(new_zoom)
    driver.camera.set_camera_world_center(vec2f(0, 0))


dragging_slider = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (
            not dragging_slider
            and event.type == pygame.MOUSEBUTTONDOWN
            and mouse_touching_slider()
        ):
            dragging_slider = True
        if dragging_slider and event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = False
        if dragging_slider and event.type == pygame.MOUSEMOTION:
            slider_x = min(max(event.pos[0], 50), 750)
            ratio = (slider_x - 50) / 700
            set_camera_to_zoom_by_ratio(ratio)

        # Handle driver after slider
        if driver.handle_event(event):
            continue

    screen.fill((50, 50, 50))
    driver.draw()

    # Draw slider
    pygame.draw.rect(screen, "black", (50, 525, 700, 25))
    pygame.draw.circle(screen, "black", (slider_x, 537.5), 30)

    location = display_font.render(str(driver.camera.topleft), False, "white")
    zoom = display_font.render(str(driver.camera.camerazoom), False, "white")

    screen.blit(location, (10, 10))
    screen.blit(zoom, (10, 25))

    pygame.display.flip()

pygame.quit()
