from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Point:
    """Одна точка карты высот."""

    x: int
    y: int
    z: int
    color: str | None = None

@dataclass
class Map:
    """Карта высот, состоящая из строк точек."""

    points: list[list[Point]]

    def __len__(self) -> int:
        """Возвращает общее количество точек на карте."""
        return sum(len(row) for row in self.points)

    def __iter__(self) -> Iterator[Point]:
        """Позволяет перебирать все точки карты."""
        for row in self.points:
            yield from row

    @property
    def width(self) -> int:
        """Возвращает количество точек в одной строке."""
        return len(self.points[0]) if self.points else 0

    @property
    def height(self) -> int:
        """Возвращает количество строк карты."""
        return len(self.points)

    def neighbors(self, x: int, y: int) -> list[Point]:
        """Возвращает соседей точки справа и снизу."""
        neighbors_list = []

        if x + 1 < self.width:
            neighbors_list.append(self.points[y][x + 1])

        if y + 1 < self.height:
            neighbors_list.append(self.points[y + 1][x])

        return neighbors_list