import sys

from PIL.ImageQt import ImageQt
from PyQt6 import QtGui, QtWidgets, uic

from main import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setFixedWidth(1000)
        self.setFixedHeight(580)
        
        # Define Attributes
        self.history = ""
        self.tags = []
        self.wars = {}
        self.battles = {}
        self.belligerents = {}

        # Assign callbacks
        self.file_button.clicked.connect(self.load_file)
        self.folder_button.clicked.connect(self.load_folder)
        self.tag_list.currentItemChanged.connect(self.select_tag)
        self.war_list.currentItemChanged.connect(self.select_war)
        self.battle_list.currentItemChanged.connect(self.select_battle)

    def load_file(self, file=None):
        if not file:
            file = str(QtWidgets.QFileDialog.getOpenFileName(self, "Select File")[0])
        if try_file(file):
            self.history = read_file(file)
            self.tags = get_tags(self.history)
            self.tag_list.addItems(self.tags)
            self.wars = get_wars(self.history)

    def load_folder(self, folder=None):
        if not folder:
            folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder"))
        if try_folder(folder):
            background = ImageQt("Victoria 2/gfx/interface/frontend_ms_bg.dds")
            battle_background = ImageQt("Victoria 2/gfx/interface/combat_end_bg.dds")
            self.background.setPixmap(QtGui.QPixmap.fromImage(background))
            self.battle_background.setPixmap(QtGui.QPixmap.fromImage(battle_background))

    def select_tag(self):
        wars = []
        for key in ["active_war", "previous_war"]:
            for war in self.wars[key]:
                belligerents, battles = view_war(self.history, war)
                for time in belligerents:
                    for side in belligerents[time]:
                        for tag in belligerents[time][side]:
                            if tag == self.tag_list.currentItem().text():
                                wars.append(war)
                                break
        self.battle_list.clear()
        self.war_list.clear()
        self.war_list.addItems(wars)

    def select_war(self):
        if self.war_list.currentItem() is None:
            pass
        else:
            self.belligerents, self.battles = view_war(self.history, self.war_list.currentItem().text())
            battles = []
            for battle, data in self.battles.items():
                battles.append(battle)
            self.battle_list.clear()
            self.battle_list.addItems(battles)

    def select_battle(self):
        if self.battle_list.currentItem() is None:
            pass
        else:
            # Assign alias
            this_battle = self.battles[self.battle_list.currentItem().text()]

            # Display name
            self.battle_name.setText("Battle of " + self.battle_list.currentItem().text())

            # Display leaders
            self.defender_leader.setText(this_battle["defender"]["leader"])
            self.attacker_leader.setText(this_battle["attacker"]["leader"])

            # Display winner
            self.winner.setText(
                this_battle["attacker" if this_battle["result"] == "yes" else "defender"]["country"] + " Won"
            )

            # Display losses
            these_initial_units = {"attacker": 0, "defender": 0}

            def sum_units(initial_units, label, side, unit_types):
                tally = 0
                for unit_type in unit_types:
                    if unit_type in this_battle[side].keys():
                        tally += this_battle[side][unit_type]
                label.setText(str(tally))
                initial_units[side] += tally
                return initial_units

            cavalry_types = ["cavalry"]
            infantry_types = ["infantry"]
            artillery_types = ["artillery"]

            all_unit_types = [
                {
                    "attacker": self.attacker_cavalry,
                    "defender": self.defender_cavalry,
                    "unit_types": cavalry_types
                },
                {
                    "attacker": self.attacker_infantry,
                    "defender": self.defender_infantry,
                    "unit_types": infantry_types
                },
                {
                    "attacker": self.attacker_artillery,
                    "defender": self.defender_artillery,
                    "unit_types": artillery_types
                }
            ]

            losses_labels = {
                "attacker": [self.attacker_initial, self.attacker_casualties, self.attacker_survivors],
                "defender": [self.defender_initial, self.defender_casualties, self.defender_survivors]
            }

            for s in ["attacker", "defender"]:
                for types in all_unit_types:
                    these_initial_units = sum_units(these_initial_units, types[s], s, types["unit_types"])
                losses_labels[s][0].setText(str(these_initial_units[s]))
                losses_labels[s][1].setText(str(this_battle[s]["losses"]))
                losses_labels[s][2].setText(str(these_initial_units[s] - this_battle[s]["losses"]))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
preset_file, preset_folder = load_presets()  # TODO: Either disable when blank, or force the loading of game files
window.load_file(preset_file)
window.load_folder(preset_folder)
window.show()
app.exec()
