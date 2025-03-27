import pytest
import pygame
import pyzer
from .common import surface_equals_snapshot

def init_driver() -> pyzer.PygameDriver:
    pygame.init()
    screen = pygame.Surface((500, 500))
    return pyzer.PygameDriver(screen)

def test_shape_implemented():
    driver = init_driver()

    try:
        pyzer.Circle(driver, (100, 100), 25)
    except TypeError:
        pytest.fail()

def test_fill_draws():
    driver = init_driver()
    pyzer.Circle(driver, (100, 100), 25, fill="red")

    driver.camera.surface.fill((0, 0, 0))
    # pixel is black
    assert surface_equals_snapshot(driver.camera.surface, "circle/test_fill_draws_0")

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "circle/test_fill_draws_1")


def test_outline_draws():
    driver = init_driver()
    pyzer.Circle(driver, (100, 100), 25, outline="green", outlineWidth=2)

    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "circle/test_outline_draws_0")

def test_translates():
    driver = init_driver()
    circle = pyzer.Circle(driver, (100, 100), 25, fill="red")

    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "circle/test_translates_0")

    circle.translate(0, 25)
    # only updates on redraw
    assert surface_equals_snapshot(driver.camera.surface, "circle/test_translates_0")

    driver.draw()
    assert surface_equals_snapshot(driver.camera.surface, "circle/test_translates_1")
