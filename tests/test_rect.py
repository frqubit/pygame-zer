import pygame
import pytest

import pygame_zer
from pygame_zer.circle import CircleHitbox
from pygame_zer.hitbox import CollideResult
from pygame_zer.line import LineHitbox
from pygame_zer.rect import RectHitbox

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


def test_hitbox_circle():
    r1 = RectHitbox((10, 10, 50, 50))
    r2 = RectHitbox((30, 30, 50, 50))
    c1 = CircleHitbox((15, 15), 5)
    c2 = CircleHitbox((20, 20), 15)
    c3 = CircleHitbox((75, 75), 5)

    assert r1.contains_hitbox(c1) == CollideResult.YES
    assert r1.contains_hitbox(c2) == CollideResult.NO
    assert r1.collides_hitbox(c2) == CollideResult.YES
    assert c2.collides_hitbox(r1) == CollideResult.YES
    assert r1.contains_hitbox(c3) == CollideResult.NO
    assert r1.collides_hitbox(c3) == CollideResult.NO
    assert r2.contains_hitbox(c3) == CollideResult.YES
    assert r2.collides_hitbox(c3) == CollideResult.YES
    assert r2.collides_hitbox(c2) == CollideResult.YES
    assert r2.collides_hitbox(c1) == CollideResult.NO


def test_hitbox_rect():
    r1 = RectHitbox((10, 10, 50, 50))
    r2 = RectHitbox((30, 30, 50, 50))
    r3 = RectHitbox((15, 15, 10, 10))
    r4 = RectHitbox((31, 31, 40, 40))

    assert r1.contains_hitbox(r2) == CollideResult.NO
    assert r1.collides_hitbox(r2) == CollideResult.YES
    assert r3.contains_hitbox(r1) == CollideResult.NO
    assert r1.contains_hitbox(r3) == CollideResult.YES
    assert r2.contains_hitbox(r3) == CollideResult.NO
    assert r4.contains_hitbox(r2) == CollideResult.NO
    assert r2.contains_hitbox(r4) == CollideResult.YES
    assert r4.collides_hitbox(r2) == CollideResult.YES


def test_hitbox_line():
    r1 = RectHitbox((10, 10, 50, 50))
    l1 = LineHitbox((12, 12), (10, 25))
    l2 = LineHitbox((8, 12), (12, 8))
    l3 = LineHitbox((9, 10.5), (11, 8.5))

    assert r1.contains_hitbox(l1) == CollideResult.YES
    assert r1.contains_hitbox(l2) == CollideResult.NO
    assert r1.collides_hitbox(l2) == CollideResult.YES
    assert r1.collides_hitbox(l3) == CollideResult.NO
