from fdf.model import Map, Point
from fdf.render import get_edges


def test_get_edges() -> None:
    """Проверяет количество рёбер квадратной карты."""
    map_data = Map([
        [Point(0, 0, 0), Point(1, 0, 1)],
        [Point(0, 1, 2), Point(1, 1, 3)],
    ])

    edges = get_edges(map_data)

    assert len(edges) == 4

def test_edges_are_unique() -> None:
    """Проверяет отсутствие повторяющихся рёбер."""
    map_data = Map([
        [Point(0, 0, 0), Point(1, 0, 1)],
        [Point(0, 1, 2), Point(1, 1, 3)],
    ])

    edges = get_edges(map_data)

    unique_edges = {
        frozenset([
            (first.x, first.y),
            (second.x, second.y),
        ])
        for first, second in edges
    }

    assert len(edges) == len(unique_edges)

def test_single_point_has_no_edges() -> None:
    """Проверяет, что у одной точки нет рёбер."""
    map_data = Map([[Point(0, 0, 5)]])

    assert get_edges(map_data) == []


