import random

import pygame
import pytest

import pygame_zer


def init_driver() -> pygame_zer.PygameDriver:
    pygame.init()
    screen = pygame.Surface((500, 500))
    return pygame_zer.PygameDriver(screen)


def test_point_conversion_works():
    driver = init_driver()

    def assert_positions_equal():
        pt = (random.randint(0, 500), random.randint(0, 500))
        conv = driver.camera.point_to_camera(driver.camera.point_to_world(pt))
        assert abs(conv[0] - pt[0]) < 0.001
        assert abs(conv[1] - pt[1]) < 0.001

    assert_positions_equal()

    driver.camera.zoom(1)

    assert_positions_equal()

    driver.camera.zoom(-1)
    driver.camera.zoom(-1)
    driver.camera.zoom(-1)

    assert_positions_equal()


def test_zoom_focuson_works():
    driver = init_driver()

    def assert_positions_close_enough(a, b):
        assert abs(a[0] - b[0]) < 0.001
        assert abs(a[0] - b[0]) < 0.001

    old_pos = driver.camera.point_to_world((10, 10))
    driver.camera.zoom_with_focus(1, (10, 10))
    assert_positions_close_enough(old_pos, driver.camera.point_to_world((10, 10)))

    old_pos = driver.camera.point_to_world((55, 25))
    driver.camera.zoom_with_focus(1, (55, 25))
    assert_positions_close_enough(old_pos, driver.camera.point_to_world((55, 25)))

    old_pos = driver.camera.point_to_world((104, 125))
    driver.camera.zoom_with_focus(-1, (104, 125))
    assert_positions_close_enough(old_pos, driver.camera.point_to_world((104, 125)))
