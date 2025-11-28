"""
My first application
"""

import toga
from toga.style.pack import COLUMN, ROW
from .pilote import Pilote

class pypilotRemote(toga.App):
    def startup(self):

        self.main_window = toga.MainWindow(title=self.formal_name)
        pilote = Pilote(self.main_window.dialog)
        self.main_window.content = pilote.get_box()
        self.main_window.show()


def main():
    return pypilotRemote()
