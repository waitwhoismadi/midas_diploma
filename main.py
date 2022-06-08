from telegram.ext import Updater
from telegram_menu import BaseMessage, TelegramMenuSession, NavigationHandler, ButtonType, navigation
from telegram_menu import MenuButton
from tests.test_connection import SecondMenuMessage
import tracker, bot, config

api_key = config.TELEGRAM_BOT_TOKEN

class StartMessage(BaseMessage):

    LABEL = "start"

    def __init__(self, navigation: NavigationHandler) -> None:
        super().__init__(navigation, StartMessage.LABEL)

    def update(self) -> str:
        second_menu = SecondMenuMessage(navigation)
        third_menu = ThirdMenuMessage(navigation)
        fourth_menu = SecondMenuMessage(navigation)
        self.add_button(label="Currencies", callback=second_menu)
        self.add_button(label="Positions", callback=third_menu)
        self.add_button(label="Trading platforms", callback=fourth_menu)
        return "Welcome to Bot Midas! Choose your actions in the menu"

class SecondMenuMessage(BaseMessage):

    LABEL = "action"


    def __init__(self) -> None:



    def update(self) -> str:
        return ":warning: Second message"

    @staticmethod
    def run_and_notify() -> str:
        return "This is a notification"


class ThirdMenuMessage(BaseMessage):

    LABEL = "action"

    def __init__(self, navigation: NavigationHandler) -> None:
        super().__init__(navigation, StartMessage.LABEL, inlined=True)

        # 'run_and_notify' function executes an action and return a string as Telegram notification.
        self.add_button(label="Action", callback=self.run_and_notify)
        # 'back' button goes back to previous menu
        self.add_button_back()
        # 'home' button goes back to main menu
        self.add_button_home()

    def update(self) -> str:
        return ":warning: Second message"

    @staticmethod
    def run_and_notify() -> str:
        return "This is a notification"


class FourthMenuMessage(BaseMessage):
    LABEL = "action"

    def __init__(self, navigation: NavigationHandler) -> None:
        super().__init__(navigation, StartMessage.LABEL, inlined=True)

        self.add_button(label="Action", callback=self.run_and_notify)
        self.add_button_back()
        self.add_button_home()

    def update(self) -> str:
        return ":warning: Second message"

    @staticmethod
    def run_and_notify() -> str:
        return "This is a notification"


TelegramMenuSession(api_key).start(StartMessage)