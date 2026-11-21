import math

import pytest

from fdf.model import Map, Point
from fdf.projection import Camera


def test_project_origin() -> None:
    """Проверяет проекцию точки с нулевыми координатами."""
    camera = Camera()

    assert camera.project(Point(0, 0, 0)) == (0.0, 0.0)

def test_project_point() -> None:
    """Проверяет математическую формулу проекции."""
    camera = Camera()

    x, y = camera.project(Point(2, 0, 0))

    assert math.isclose(x, math.sqrt(3))
    assert math.isclose(y, 1.0)

def test_project_height() -> None:
    """Проверяет влияние высоты на проекцию."""
    camera = Camera(z_scale=2.0)

    x, y = camera.project(Point(0, 0, 3))

    assert x == 0.0
    assert y == -6.0

def test_camera_fit() -> None:
    """Проверяет автоматическое масштабирование и центрирование."""
    map_data = Map([
        [Point(0, 0, 0), Point(1, 0, 0)],
        [Point(0, 1, 0), Point(1, 1, 0)],
    ])

    camera = Camera.fit(map_data, 800, 600)

    projected_points = [
        camera.project(point) for point in map_data
    ]

    min_x = min(point[0] for point in projected_points)
    max_x = max(point[0] for point in projected_points)
    min_y = min(point[1] for point in projected_points)
    max_y = max(point[1] for point in projected_points)

    assert math.isclose((min_x + max_x) / 2, 400)
    assert math.isclose((min_y + max_y) / 2, 300)

def test_camera_fit_empty_map() -> None:
    """Проверяет отказ от размещения пустой карты."""
    with pytest.raises(ValueError):
        Camera.fit(Map([]), 800, 600)

def test_camera_fit_invalid_size() -> None:
    """Проверяет обработку неправильного размера окна."""
    map_data = Map([[Point(0, 0, 0)]])

    with pytest.raises(ValueError):
        Camera.fit(map_data, 0, 600)