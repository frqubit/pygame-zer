import pytest
import pygame
import pygame_zer
from .common import surface_equals_snapshot

def init_driver() -> pygame_zer.PygameDriver:
    pygame.init()
    screen = pygame.Surface((500, 500))
    return pygame_zer.PygameDriver(screen)

def test_shape_implemented():
    driver = init_driver()

    try:
        pygame_zer.Rect(driver, (100, 100, 50, 50))
    except TypeError:
        pytest.fail()

def test_fill_draws():
    driver = init_driver()
    pygame_zer.Rect(driver, (100, 100, 50, 78), fill="red")

    driver.camera.surface.fill((0, 0, 0))
    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "rect/test_fill_draws_0")


def test_outline_draws():
    driver = init_driver()
    pygame_zer.Rect(driver, (100, 100, 50, 76), outline="green", outlineWidth=2)
    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "rect/test_outline_draws_0")

def test_translates():
    driver = init_driver()
    rect = pygame_zer.Rect(driver, (100, 125, 65, 30), fill="red")

    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "rect/test_translates_0")

    rect.translate(0, 100)
    # only updates on redraw
    assert surface_equals_snapshot(driver.camera.surface, "rect/test_translates_0")

    driver.draw()
    assert surface_equals_snapshot(driver.camera.surface, "rect/test_translates_1")
