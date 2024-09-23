import pywinauto.mouse
from auto_fcmobile.commons import Application, Coordinate, Page, Area
import pywinauto


class MainMenu(Page):
    def __init__(self, application: Application) -> None:
        super().__init__(application)

        self.add_linked_page(Market, 0.50, 0.95)


class Market(Page):
    def __init__(self, application: Application) -> None:
        super().__init__(application)

        self.add_linked_page(MainMenu, 0.95, 0.05)


class FCMobileApplication(Application):
    def __init__(self, windows_name) -> None:
        app = pywinauto.Application().connect(title=windows_name)

        screen = app[windows_name]["HD-Player"]

        app_rect = screen.rectangle()
        area = Area(
            app_rect.left,
            app_rect.top,
            app_rect.right,
            app_rect.bottom,
        )

        super().__init__(area)

        self.set_page(MainMenu(self), current=True)
        self.set_page(Market(self))

    def click_action(self, coordinate: Coordinate) -> None:
        pywinauto.mouse.click(button="left", coords=coordinate.as_tuple())
