import pygame
import pytest

import pygame_zer
from pygame_zer.hitbox import CollideResult
from pygame_zer.line import LineHitbox

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


def test_hitbox_point():
    l1 = LineHitbox((10, 10), (25, 25))
    l2 = LineHitbox((10, 10), (10, 25))

    assert l1.contains_point((10, 10)) == CollideResult.YES
    assert l2.contains_point((10, 10)) == CollideResult.YES
    assert l1.contains_point((18, 18)) == CollideResult.YES
    assert l1.contains_point((18, 19)) == CollideResult.NO
    assert l1.contains_point((30, 30)) == CollideResult.NO
    assert l2.contains_point((10, 24)) == CollideResult.YES
    assert l2.contains_point((12, 24)) == CollideResult.NO
    assert l2.contains_point((10, 28)) == CollideResult.NO
    assert l2.contains_point((10, 8)) == CollideResult.NO


def test_hitbox_line():
    l1 = LineHitbox((10, 10), (25, 25))
    l2 = LineHitbox((15, 15), (25, 25))
    l3 = LineHitbox((15, 8), (25, 20))
    l4 = LineHitbox((15, 8), (25, 30))
    l5 = LineHitbox((20, 15), (31, 35))

    assert l1.contains_hitbox(l2) == CollideResult.YES
    assert l2.contains_hitbox(l1) == CollideResult.NO
    assert l2.collides_hitbox(l1) == CollideResult.YES
    assert l3.collides_hitbox(l2) == CollideResult.NO
    assert l1.collides_hitbox(l3) == CollideResult.NO
    assert l1.contains_hitbox(l3) == CollideResult.NO
    assert l3.collides_hitbox(l4) == CollideResult.YES
    assert l1.collides_hitbox(l4) == CollideResult.YES
    assert l4.collides_hitbox(l5) == CollideResult.NO
    # Barely doesn't
    assert l1.collides_hitbox(l5) == CollideResult.NO

    l6 = LineHitbox((10, 30), (10, 10))
    l7 = LineHitbox((10, 25), (10, 35))
    l8 = LineHitbox((12, 25), (12, 35))

    assert l6.collides_hitbox(l7) == CollideResult.YES
    assert l7.collides_hitbox(l8) == CollideResult.NO
    assert l1.collides_hitbox(l6) == CollideResult.YES
    assert l1.collides_hitbox(l8) == CollideResult.NO
