import math
from dataclasses import dataclass

from fdf.model import Map, Point


@dataclass
class Camera:
    """Камера для преобразования координат карты."""

    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    z_scale: float = 1.0

    def project(self, point: Point) -> tuple[float, float]:
        """Преобразует 3D-координаты точки в 2D-координаты экрана."""
        cos_30 = math.cos(math.radians(30))
        sin_30 = math.sin(math.radians(30))

        projected_x = (point.x - point.y) * cos_30
        projected_y = (
            (point.x + point.y) * sin_30
            - point.z * self.z_scale
        )

        screen_x = projected_x * self.scale + self.offset_x
        screen_y = projected_y * self.scale + self.offset_y

        return screen_x, screen_y

    @classmethod
    def fit(cls, map_data: Map, width: int, height: int) -> "Camera":
        """Подбирает масштаб и смещение для размещения карты в окне."""
        if width <= 0 or height <= 0:
            raise ValueError("Размеры окна должны быть положительными.")

        points = list(map_data)

        if not points:
            raise ValueError("Нельзя разместить пустую карту.")

        camera = cls()

        projected_points = [
            camera.project(point) for point in points
        ]

        min_x = min(point[0] for point in projected_points)
        max_x = max(point[0] for point in projected_points)
        min_y = min(point[1] for point in projected_points)
        max_y = max(point[1] for point in projected_points)

        map_width = max_x - min_x
        map_height = max_y - min_y

        scale_x = width / map_width if map_width > 0 else float("inf")
        scale_y = height / map_height if map_height > 0 else float("inf")

        scale = min(scale_x, scale_y) * 0.9

        if math.isinf(scale):
            scale = 1.0

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        return cls(
            scale=scale,
            offset_x=width / 2 - center_x * scale,
            offset_y=height / 2 - center_y * scale,
        )