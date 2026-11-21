import tkinter as tk

from fdf.model import Map
from fdf.projection import Camera
from fdf.render import get_edges


class App:
    """Графический интерфейс для отображения карты высот."""

    def __init__(self, map_data: Map) -> None:
        self.map_data = map_data
        self.zoom = 1.0

        self.root = tk.Tk()
        self.root.title("FdF — карта высот")
        self.root.geometry("900x700")

        self.canvas = tk.Canvas(
            self.root,
            background="#202020",
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Escape>", self._on_escape)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<MouseWheel>", self._on_zoom)

    def _on_escape(self, event: tk.Event) -> None:
        """Закрывает окно при нажатии Escape."""
        self.root.destroy()

    def _on_resize(self, event: tk.Event) -> None:
        """Перерисовывает карту при изменении размера окна."""
        self.draw()

    def _on_zoom(self, event: tk.Event) -> None:
        """Приближает или отдаляет карту колёсиком мыши."""
        if event.delta > 0:
            self.zoom = min(self.zoom * 1.1, 5.0)
        elif event.delta < 0:
            self.zoom = max(self.zoom / 1.1, 0.2)

        self.draw()

    def draw(self) -> None:
        """Рисует каркас карты на холсте."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        camera = Camera.fit(self.map_data, width, height)

        camera.scale *= self.zoom
        camera.offset_x = width / 2 + (
            camera.offset_x - width / 2
        ) * self.zoom
        camera.offset_y = height / 2 + (
            camera.offset_y - height / 2
        ) * self.zoom

        self.canvas.delete("all")

        for first, second in get_edges(self.map_data):
            x1, y1 = camera.project(first)
            x2, y2 = camera.project(second)

            color = first.color or second.color or "#FFFFFF"

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                width=2,
            )

    def run(self) -> None:
        """Запускает главный цикл графического интерфейса."""
        self.root.mainloop()





