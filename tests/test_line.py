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
        pygame_zer.Line(driver, (100, 100), (50, 50))
    except TypeError:
        pytest.fail()

def test_fill_draws():
    driver = init_driver()
    pygame_zer.Line(driver, (100, 100), (50, 50))

    driver.camera.surface.fill((0, 0, 0))
    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "line/test_fill_draws_0")

def test_translates():
    driver = init_driver()
    line = pygame_zer.Line(driver, (100, 100), (50, 75))

    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "line/test_translates_0")

    line.translate(0, 100)
    # only updates on redraw
    assert surface_equals_snapshot(driver.camera.surface, "line/test_translates_0")

    driver.draw()
    assert surface_equals_snapshot(driver.camera.surface, "line/test_translates_1")
