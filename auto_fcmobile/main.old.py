from PIL import ImageGrab
from pywinauto import Application, mouse
from time import sleep
import random


ACTION_DELAY = 0.5
WIN_NAME = "BlueStacks App Player"
# WIN_NAME = "bluestacks-services"
# WIN_NAME = "BlueStacks Keymap Overlay"


class Coordinates:
    def __init__(self, left, top, right, bottom) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

        self.width = right - left
        self.height = bottom - top

    def as_tuple(self):
        return (self.left, self.top, self.right, self.bottom)


class FCMobileBot:
    def __init__(self, coordinates: Coordinates):
        self.coordinates = coordinates

    def compute_coordinate(self, x_offset, y_offset):
        x_noise = random.uniform(-0.03, 0.03)
        y_noise = random.uniform(-0.03, 0.03)
        print(f"{x_noise=}, {y_noise=}")
        x = self.coordinates.left + int(self.coordinates.width * (x_offset + x_noise))
        y = self.coordinates.top + int(self.coordinates.height * (y_offset + y_noise))
        return x, y

    def open_menu(self):
        yield self.compute_coordinate(0.95, 0.05)

    def open_market_from_menu(self):
        yield self.compute_coordinate(0.50, 0.95)

    def set_market_order_asc(self):
        yield self.compute_coordinate(0.80, 0.20)
        yield self.compute_coordinate(0.80, 0.60)

    def open_orders(self):
        yield self.compute_coordinate(0.70, 0.13)

    def open_searches(self):
        yield self.compute_coordinate(0.90, 0.13)


def execute_action(action):
    for c in action:
        mouse.click(coords=c)
        sleep(ACTION_DELAY)


def main():
    app = Application().connect(title=WIN_NAME)

    screen = app[WIN_NAME]["HD-Player"]

    app_rect = screen.rectangle()
    coordinates = Coordinates(
        app_rect.left,
        app_rect.top,
        app_rect.right,
        app_rect.bottom,
    )
    print(coordinates.as_tuple())

    bot = FCMobileBot(coordinates)

    # execute_action(bot.open_orders())
    execute_action(bot.open_searches())
    execute_action(bot.set_market_order_asc())

    # screeshot = ImageGrab.grab(coordinates.as_tuple())
    # screeshot.show()
