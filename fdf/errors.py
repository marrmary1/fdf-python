class FdfError(Exception):
    """Базовая ошибка программы FdF."""

class MapFormatError(FdfError):
    """Ошибка формата файла карты высот."""
    