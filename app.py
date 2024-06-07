import os
import sys

from PyQt6 import QtWidgets, uic

import main


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.console = main.Main()

        # Data Loading
        self.saveGameButton.clicked.connect(self.load_file)
        self.gameFolderButton.clicked.connect(self.load_folder)
        self.loadModButton.clicked.connect(lambda: self.move_mod(self.unloadedModsList, self.loadedModsList))
        self.unloadModButton.clicked.connect(lambda: self.move_mod(self.loadedModsList, self.unloadedModsList))

    def load_file(self):
        save_file = str(QtWidgets.QFileDialog.getOpenFileName(self, "Select File")[0])
        if self.console.read_file(save_file):
            self.saveGameLabel.setText(save_file)
        else:
            self.saveGameLabel.setText("Invalid Victoria 2 save game; please try again")

    def load_folder(self):
        game_folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder"))
        if self.console.read_folder(game_folder):
            mods = []
            for entry in os.scandir(game_folder + "/mod"):
                if entry.is_dir():
                    mods.append(entry.name)
            self.unloadedModsList.addItems(mods)
            self.gameFolderLabel.setText(game_folder)
        else:
            self.gameFolderLabel.setText("Invalid Victoria 2 installation; please try again")

    @staticmethod
    def move_mod(mv_from, mv_to):
        mv_to.addItem(mv_from.takeItem(mv_from.currentRow()))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
