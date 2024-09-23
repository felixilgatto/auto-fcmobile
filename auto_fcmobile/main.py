from auto_fcmobile.commons import Area
from auto_fcmobile.fcmobile import FCMobileApplication, Market
from pywinauto import Application

ACTION_DELAY = 0.5
WIN_NAME = "BlueStacks App Player"


def main():

    app = FCMobileApplication(WIN_NAME)

    app.goto(Market)
    app.goto(Market)
