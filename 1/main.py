import os
import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from controller.lab_controller import LabController
from model.lab_model import LabModel


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    model = LabModel()
    LabController(model)

    random.seed()

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
