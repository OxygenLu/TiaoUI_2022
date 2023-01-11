import sys

from PyQt5.QtWidgets import QApplication

from interface import Window
from process import Identify
from client import Client
from qt_material import apply_stylesheet
import os

envpath = '~/.local/lib/python3.10/site-packages/cv2/qt/plugins/platforms'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = envpath

extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'Roboto',
}

class App:
    def __init__(self):
        super().__init__()
        self.qapp = QApplication(sys.argv)
        self.win = Window(self)
        self.win.show()
        self.identify = Identify(self.win)
        self.client = Client(self)

    def run(self, has_father_window=False):
        self.identify.start()
        self.client.start()
        if not has_father_window:
            apply_stylesheet(self.qapp, theme='light_blue.xml', invert_secondary=True, extra=extra)
            sys.exit(self.qapp.exec_())


if __name__ == '__main__':
    app = App()
    app.run()