"""
My first application
"""

import toga
from toga.style.pack import COLUMN, ROW
from .pilote import Pilote
from .ipserver import Ipserver

class pypilotRemote(toga.App):
    def startup(self):

        PYPILOTE_SERVICE = "_pypilot._tcp.local."
                        
        self.main_window = toga.MainWindow(title="Pypilote")
        Ipserver(PYPILOTE_SERVICE,self.__initialize_main_page)
        
        
    def __initialize_main_page(self,url):
        pilote = Pilote(url)
        self.main_window.content = pilote.get_box()
        self.main_window.show()

def main():
    return pypilotRemote()
