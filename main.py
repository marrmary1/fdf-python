import argparse
import sys

from fdf.app import App
from fdf.errors import FdfError
from fdf.parser import parse_map


def main() -> int:
    """Запускает программу FdF."""
    parser = argparse.ArgumentParser(
        description="Просмотр каркасной 3D-модели карты высот."
    )
    parser.add_argument("file", help="Путь к файлу карты .fdf")

    if (
        len(sys.argv) != 2
        and "-h" not in sys.argv
        and "--help" not in sys.argv
    ):
        parser.print_help(file=sys.stderr)
        return 2

    args = parser.parse_args()

    try:
        map_data = parse_map(args.file)
    except (FdfError, OSError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    app = App(map_data)
    app.run()

    return 0

if __name__ == "__main__":
    sys.exit(main())