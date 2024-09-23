from dataclasses import dataclass
from functools import wraps


@dataclass
class Coordinate:
    x: int
    y: int

    @classmethod
    def from_percent(cls, x_percent: float, y_percent: float, width: int, height: int):
        return cls(int(x_percent * width), int(y_percent * height))

    def as_tuple(self):
        return self.x, self.y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)


@dataclass
class Area:
    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self):
        return self.right - self.left

    @property
    def topleft(self):
        return Coordinate(self.left, self.top)

    @property
    def bottomright(self):
        return Coordinate(self.right, self.bottom)

    @property
    def height(self):
        return self.bottom - self.top

    def as_tuple(self):
        return self.left, self.top, self.right, self.bottom


class Application:
    _pages: dict[str, "Page"] = {}
    _current_page: "Page"
    area: Area

    def __init__(self, area: Area) -> None:
        self.area = area

    def set_page(self, page: "Page", current=False):
        self._pages[type(page).__name__] = page
        if current:
            self._current_page = page

    def get_page(self, name: str):
        return self._pages[name]

    def goto(self, page: "Page"):
        if page not in self._current_page._links:
            raise ValueError(f"{page} is not linked to {self}")

        self.click_action(self._current_page._links[page])

        self._current_page = page

    def click_action(self, coordinate: Coordinate) -> None:
        raise NotImplementedError


class Page:
    _links: dict["Page", Coordinate] = {}

    def __init__(self, application: "Application") -> None:
        self.application: "Application" = application

    def add_linked_page(self, page_cls: "Page", x_percent: float, y_percent: float):
        self._links[page_cls] = self.application.area.topleft + Coordinate.from_percent(
            x_percent,
            y_percent,
            self.application.area.width,
            self.application.area.height,
        )
