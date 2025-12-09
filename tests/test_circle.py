import pygame
import pytest

import pygame_zer
from pygame_zer.circle import CircleHitbox
from pygame_zer.hitbox import CollideResult

from .common import surface_equals_snapshot


def init_driver() -> pygame_zer.PygameDriver:
    pygame.init()
    screen = pygame.Surface((500, 500))
    return pygame_zer.PygameDriver(screen)


def test_shape_implemented():
    driver = init_driver()

    try:
        pygame_zer.Circle(driver, (100, 100), 25)
    except TypeError:
        pytest.fail()


def test_fill_draws():
    driver = init_driver()
    pygame_zer.Circle(driver, (100, 100), 25, fill="red")

    driver.camera.surface.fill((0, 0, 0))
    # pixel is black
    assert surface_equals_snapshot(driver.camera.surface, "circle/test_fill_draws_0")

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "circle/test_fill_draws_1")


def test_outline_draws():
    driver = init_driver()
    pygame_zer.Circle(driver, (100, 100), 25, outline="green", outlineWidth=2)

    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "circle/test_outline_draws_0")


def test_translates():
    driver = init_driver()
    circle = pygame_zer.Circle(driver, (100, 100), 25, fill="red")

    driver.camera.surface.fill((0, 0, 0))

    driver.draw()

    assert surface_equals_snapshot(driver.camera.surface, "circle/test_translates_0")

    circle.translate(0, 25)
    # only updates on redraw
    assert surface_equals_snapshot(driver.camera.surface, "circle/test_translates_0")

    driver.draw()
    assert surface_equals_snapshot(driver.camera.surface, "circle/test_translates_1")


def test_contains_circle():
    c1 = CircleHitbox((15, 15), 10)
    c2 = CircleHitbox((18, 19), 5)
    c3 = CircleHitbox((0, 0), 100)

    assert c1.contains_hitbox(c2) == CollideResult.YES
    assert c2.contains_hitbox(c1) == CollideResult.NO
    assert c3.contains_hitbox(c1) == CollideResult.YES
    assert c3.contains_hitbox(c2) == CollideResult.YES


def test_collides_circle():
    c1 = CircleHitbox((15, 15), 10)
    c2 = CircleHitbox((24, 27), 5)
    c3 = CircleHitbox((35, 35), 10)

    assert c1.collides_hitbox(c2) == CollideResult.YES
    assert c2.collides_hitbox(c1) == CollideResult.YES
    assert c1.collides_hitbox(c3) == CollideResult.NO
    assert c2.collides_hitbox(c3) == CollideResult.YES
