from pathlib import Path

from fdf.errors import MapFormatError
from fdf.model import Map, Point


def parse_map(file_path: str | Path) -> Map:
    """Читает файл FDF и создаёт карту высот."""

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    points: list[list[Point]] = []
    expected_width: int | None = None

    for y, line in enumerate(lines, start=1):
        values = line.split()

        if not values:
            continue

        row: list[Point] = []

        for x, value in enumerate(values):
            parts = value.split(",")

            if len(parts) > 2:
                raise MapFormatError(
                    f"Строка {y}, колонка {x + 1}: "
                    "слишком много частей у точки."
                )

            try:
                z = int(parts[0])
            except ValueError:
                raise MapFormatError(
                    f"Строка {y}, колонка {x + 1}: "
                    "высота должна быть целым числом."
                ) from None

            color = None

            if len(parts) == 2:
                raw_color = parts[1]

                if (
                    raw_color[:2].lower() != "0x"
                    or not 1 <= len(raw_color[2:]) <= 6
                    or any(
                        char not in "0123456789abcdefABCDEF"
                        for char in raw_color[2:]
                    )
                ):
                    raise MapFormatError(
                        f"Строка {y}, колонка {x + 1}: "
                        "некорректный цвет."
                    )

                color = f"#{int(raw_color, 0):06X}"

            row.append(Point(x=x, y=len(points), z=z, color=color))

        if expected_width is None:
            expected_width = len(row)
        elif len(row) != expected_width:
            raise MapFormatError(
                f"Строка {y}: разная длина строк карты."
            )

        points.append(row)

    if not points:
        raise MapFormatError("Файл карты пуст.")

    return Map(points)