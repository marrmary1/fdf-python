import pytest

from fdf.errors import MapFormatError
from fdf.parser import parse_map


def test_parse_map() -> None:
    """Проверяет чтение правильной карты."""
    map_data = parse_map("maps/example.fdf")

    assert map_data.width == 3
    assert map_data.height == 3
    assert len(map_data) == 9
    assert map_data.points[0][0].z == 0
    assert map_data.points[0][1].z == 1
    assert map_data.points[0][1].color == "#FF0000"
    assert map_data.points[2][2].z == 4

def test_empty_file(tmp_path) -> None:
    """Проверяет обработку пустого файла."""
    file_path = tmp_path / "empty.fdf"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(MapFormatError):
        parse_map(file_path)

def test_invalid_height(tmp_path) -> None:
    """Проверяет обработку неправильной высоты."""
    file_path = tmp_path / "invalid.fdf"
    file_path.write_text("1 abc 3", encoding="utf-8")

    with pytest.raises(MapFormatError):
        parse_map(file_path)

def test_invalid_color(tmp_path) -> None:
    """Проверяет обработку неправильного цвета."""
    file_path = tmp_path / "color.fdf"
    file_path.write_text("1,0xGGGGGG 2", encoding="utf-8")

    with pytest.raises(MapFormatError):
        parse_map(file_path)

def test_different_row_lengths(tmp_path) -> None:
    """Проверяет, что все строки имеют одинаковую длину."""
    file_path = tmp_path / "rows.fdf"
    file_path.write_text("1 2 3\n4 5", encoding="utf-8")

    with pytest.raises(MapFormatError):
        parse_map(file_path)

def test_negative_heights(tmp_path) -> None:
    """Проверяет чтение отрицательных высот."""
    file_path = tmp_path / "negative.fdf"
    file_path.write_text("-5 0 7", encoding="utf-8")

    map_data = parse_map(file_path)

    assert map_data.points[0][0].z == -5
    assert map_data.points[0][1].z == 0
    assert map_data.points[0][2].z == 7

def test_short_color(tmp_path) -> None:
    """Проверяет преобразование короткой записи цвета."""
    file_path = tmp_path / "short_color.fdf"
    file_path.write_text("1,0xF", encoding="utf-8")

    map_data = parse_map(file_path)

    assert map_data.points[0][0].color == "#00000F"

def test_trailing_empty_lines(tmp_path) -> None:
    """Проверяет игнорирование пустых строк в конце файла."""
    file_path = tmp_path / "empty_lines.fdf"
    file_path.write_text("1 2\n3 4\n\n", encoding="utf-8")

    map_data = parse_map(file_path)

    assert map_data.width == 2
    assert map_data.height == 2
    assert len(map_data) == 4

def test_missing_file() -> None:
    """Проверяет ошибку при отсутствии файла."""
    with pytest.raises(OSError):
        parse_map("maps/missing.fdf")

