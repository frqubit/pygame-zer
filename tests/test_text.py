import pygame
import pygame.freetype
import pytest

import pygame_zer

from .common import surface_equals_snapshot


def init_driver() -> pygame_zer.PygameDriver:
    pygame.init()
    screen = pygame.Surface((500, 500))
    return pygame_zer.PygameDriver(screen)


def test_shape_implemented():
    driver = init_driver()

    try:
        font = pygame.freetype.SysFont("Arial", 50)
        pygame_zer.Text(driver, (100, 100), font, "HI!")
    except TypeError:
        pytest.fail()


def test_fill_draws():
    driver = init_driver()
    font = pygame.freetype.SysFont("Arial", 50)
    pygame_zer.Text(driver, (100, 100), font, "HI!", fill="red")

    driver.camera.surface.fill((0, 0, 0))
    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "text/test_fill_draws_0")


def test_translates():
    driver = init_driver()
    font = pygame.freetype.SysFont("Arial", 50)
    text = pygame_zer.Text(driver, (100, 100), font, "HI!", fill="red")

    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "text/test_translates_0")

    text.translate(0, 100)
    # only updates on redraw
    assert surface_equals_snapshot(driver.camera.surface, "text/test_translates_0")

    driver.draw()
    assert surface_equals_snapshot(driver.camera.surface, "text/test_translates_1")
