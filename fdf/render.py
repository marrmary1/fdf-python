from fdf.model import Map, Point


def get_edges(map_data: Map) -> list[tuple[Point, Point]]:
    """Возвращает все рёбра карты без повторений."""

    edges = []

    for point in map_data:
        for neighbor in map_data.neighbors(point.x, point.y):
            edges.append((point, neighbor))

    return edges