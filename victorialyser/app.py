from pathlib import Path
import sys

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QIcon, QPixmap, QTransform

from victorialyser import main


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path("%s/main.ui" % Path(__file__).parent), self)
        self.setFixedWidth(1000)
        self.setFixedHeight(580)
        
        # Define attributes
        self.folder = ""
        self.history = ""
        self.keys = []
        self.tags = {}
        self.wars = {}
        self.battles = {}
        self.belligerents = {}

        # Assign callbacks
        self.file_button.clicked.connect(self.load_file)
        self.folder_button.clicked.connect(self.load_folder)
        self.tag_search.textChanged.connect(lambda: self.filter_list(self.tag_list, self.tag_search))
        self.war_search.textChanged.connect(lambda: self.filter_list(self.war_list, self.war_search))
        self.battle_search.textChanged.connect(lambda: self.filter_list(self.battle_list, self.battle_search))
        self.tag_list.currentItemChanged.connect(self.select_tag)
        self.war_list.currentItemChanged.connect(self.select_war)
        self.battle_list.currentItemChanged.connect(self.select_battle)

    def _hide_banner(self, show_banner=None):
        self.land_battle_won.hide()
        self.land_battle_lost.hide()
        self.naval_battle_won.hide()
        self.naval_battle_lost.hide()
        if show_banner is not None:
            show_banner.show()

    def _hide_units(self, show_units=None):
        self.defender_cavalry_unit.hide()
        self.defender_infantry_unit.hide()
        self.defender_artillery_unit.hide()
        self.defender_heavy_ships.hide()
        self.defender_light_ships.hide()
        self.defender_transports.hide()
        self.attacker_cavalry_unit.hide()
        self.attacker_infantry_unit.hide()
        self.attacker_artillery_unit.hide()
        self.attacker_heavy_ships.hide()
        self.attacker_light_ships.hide()
        self.attacker_transports.hide()
        if show_units is not None:
            for unit in show_units:
                unit.show()

    def _hide_all(self):
        self._hide_banner()
        self._hide_units()
        self.defender_flag.setPixmap(QPixmap())
        self.attacker_flag.setPixmap(QPixmap())
        self.battle_name.setText("")
        self.defender_leader.setText("")
        self.attacker_leader.setText("")
        self.winner.setText("")
        for widget in self.defender_losses.children():
            widget.setText("")
        for widget in self.attacker_losses.children():
            widget.setText("")
        self.tag_list.clear()
        self.war_list.clear()
        self.battle_list.clear()

    def load_file(self, file=None):
        if not file:
            file = str(QtWidgets.QFileDialog.getOpenFileName(self, "Select File")[0])
        if main.try_file(file):
            self._hide_all()
            self.history, self.keys = main.read_file(file)
            self.tag_list.clear()
            self.tags = main.read_tags(self.folder, main.get_tags(self.history, self.keys))
            for tag in self.tags.keys():
                self.tag_list.addItem(tag)
            self.war_list.clear()
            self.wars = main.get_wars(self.history, self.keys)
            self.battle_list.clear()

    def load_folder(self, folder=None, tries=0):
        if not folder:
            folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder"))
        if main.try_folder(folder):
            self.folder = folder

            background = ImageQt(Path("%s/gfx/interface/frontend_ms_bg.dds" % self.folder))
            battle_background = ImageQt(Path("%s/gfx/interface/combat_end_bg.dds" % self.folder))
            button = ImageQt(Path("%s/gfx/interface/diplo_addtowar.dds" % self.folder))
            land_battle_won = ImageQt(Path("%s/gfx/interface/combat_end_land_won.dds" % self.folder))
            land_battle_lost = ImageQt(Path("%s/gfx/interface/combat_end_land_lost.dds" % self.folder))
            naval_battle_won = ImageQt(Path("%s/gfx/interface/combat_end_naval_won.dds" % self.folder))
            naval_battle_lost = ImageQt(Path("%s/gfx/interface/combat_end_naval_lost.dds" % self.folder))

            self.background.setPixmap(QPixmap.fromImage(background))
            self.battle_background.setPixmap(QPixmap.fromImage(battle_background))
            self.file_button.setIcon(QIcon(QPixmap.fromImage(button)))
            self.folder_button.setIcon(QIcon(QPixmap.fromImage(button)))

            def draw_units(image, seeds, plant=(0, 0, 0, 0)):
                image = Image.open(image).convert("RGBA")
                for seed in seeds:
                    ImageDraw.floodfill(image, seed, plant, thresh=50)
                return ImageQt(image)

            cavalry = QPixmap.fromImage(
                draw_units(Path("%s/gfx/interface/unit_folder_army_2_cavalry.dds" % self.folder),
                           [(37, 4), (37, 34), (64, 4)])).copy(QRect(37, 4, 28, 28))
            infantry = QPixmap.fromImage(
                draw_units(Path("%s/gfx/interface/unit_folder_army_1_infantry.dds" % self.folder),
                           [(37, 4), (37, 34), (64, 4), (47, 4)])).copy(QRect(37, 4, 28, 28))
            artillery = QPixmap.fromImage(
                draw_units(Path("%s/gfx/interface/unit_folder_army_3_artillery.dds" % self.folder),
                           [(37, 4), (37, 34)])).copy(QRect(37, 4, 28, 28))
            heavy_ships = QPixmap.fromImage(
                draw_units(Path("%s/gfx/interface/unit_folder_navy_2_manowar.dds" % self.folder),
                           [(41, 4), (41, 34), (72, 4)])).copy(QRect(41, 4, 32, 28))
            light_ships = QPixmap.fromImage(
                draw_units(Path("%s/gfx/interface/unit_folder_navy_1_frigate.dds" % self.folder),
                           [(41, 4), (41, 34)])).copy(QRect(41, 4, 32, 28))
            transports = QPixmap.fromImage(
                draw_units(Path("%s/gfx/interface/unit_folder_navy_0_clipper_transport.dds" % self.folder),
                           [(41, 4), (41, 34)])).copy(QRect(41, 4, 32, 28))

            self.defender_cavalry_unit.setPixmap(cavalry)
            self.defender_infantry_unit.setPixmap(infantry)
            self.defender_artillery_unit.setPixmap(artillery)
            self.defender_heavy_ships.setPixmap(heavy_ships)
            self.defender_light_ships.setPixmap(light_ships)
            self.defender_transports.setPixmap(transports)
            self.attacker_cavalry_unit.setPixmap(cavalry)
            self.attacker_infantry_unit.setPixmap(infantry)
            self.attacker_artillery_unit.setPixmap(artillery)
            self.attacker_heavy_ships.setPixmap(heavy_ships)
            self.attacker_light_ships.setPixmap(light_ships)
            self.attacker_transports.setPixmap(transports)
            self._hide_units()

            self.land_battle_won.setPixmap(QPixmap.fromImage(land_battle_won))
            self.land_battle_lost.setPixmap(QPixmap.fromImage(land_battle_lost))
            self.naval_battle_won.setPixmap(QPixmap.fromImage(naval_battle_won))
            self.naval_battle_lost.setPixmap(QPixmap.fromImage(naval_battle_lost))
            self._hide_banner()
        else:
            tries += 1
            if tries < 3:
                self.load_folder(tries=tries)

    @staticmethod
    def filter_list(list_items, search):
        for item in range(list_items.count()):
            if search.text().lower() in list_items.item(item).text().lower():
                list_items.item(item).setHidden(False)
            else:
                list_items.item(item).setHidden(True)

    def select_tag(self):
        if self.tag_list.currentItem() is None:
            pass
        else:
            wars = []
            for key in self.keys:
                for war in self.wars[key]:
                    belligerents, battles = main.view_war(self.history, war, self.keys)
                    for time in belligerents:
                        for side in belligerents[time]:
                            for tag in belligerents[time][side]:
                                if tag == self.tags[self.tag_list.currentItem().text()]:
                                    wars.append(war)
                                    break
            self.battle_list.clear()
            self.war_list.clear()
            self.war_list.addItems(wars)

    def select_war(self):
        if self.war_list.currentItem() is None:
            pass
        else:
            self.belligerents, self.battles = main.view_war(self.history, self.war_list.currentItem().text(), self.keys)
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
            for tag in self.tags:
                if self.tags[tag] == this_battle["attacker" if this_battle["result"] == "yes" else "defender"]["country"]:
                    self.winner.setText("%s Won" % tag)

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

            cavalry_types = ["cavalry", "cuirassier", "dragoon", "hussar", "plane"]
            infantry_types = ["infantry", "guard", "irregular"]
            artillery_types = ["artillery", "engineer", "tank"]
            heavy_ship_types = ["battleship", "dreadnought", "ironclad", "manowar", "monitor"]
            light_ship_types = ["commerce_raider", "cruiser", "frigate"]
            transport_types = ["clipper_transport", "steam_transport"]

            all_unit_types = [
                {
                    "attacker": self.attacker_cavalry,
                    "defender": self.defender_cavalry,
                    "unit_types": cavalry_types + heavy_ship_types
                },
                {
                    "attacker": self.attacker_infantry,
                    "defender": self.defender_infantry,
                    "unit_types": infantry_types + light_ship_types
                },
                {
                    "attacker": self.attacker_artillery,
                    "defender": self.defender_artillery,
                    "unit_types": artillery_types + transport_types
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
                losses_labels[s][1].setText("-%s" % str(this_battle[s]["losses"]))
                losses_labels[s][2].setText(str(these_initial_units[s] - this_battle[s]["losses"]))

            # Display stack-wipe
            if self.defender_casualties.text() == "-0" and self.attacker_casualties.text() == "-0":
                if this_battle["result"] == "yes":
                    self.defender_casualties.setText("Stack Wipe")
                    self.defender_survivors.setText("0")
                else:
                    self.attacker_casualties.setText("Stack Wipe")
                    self.attacker_survivors.setText("0")

            # Display graphics
            naval = False
            for unit_type in heavy_ship_types + light_ship_types + transport_types:
                if unit_type in this_battle["attacker"].keys() or unit_type in this_battle["defender"].keys():
                    naval = True
                    break
            if naval:
                self._hide_units([self.defender_heavy_ships,
                                  self.attacker_heavy_ships,
                                  self.defender_light_ships,
                                  self.attacker_light_ships,
                                  self.defender_transports,
                                  self.attacker_transports])
                self._hide_banner(self.naval_battle_won if this_battle["result"] == "yes" else self.naval_battle_lost)
            else:
                self._hide_units([self.defender_cavalry_unit,
                                  self.attacker_cavalry_unit,
                                  self.defender_infantry_unit,
                                  self.attacker_infantry_unit,
                                  self.defender_artillery_unit,
                                  self.attacker_artillery_unit])
                self._hide_banner(self.land_battle_won if this_battle["result"] == "yes" else self.land_battle_lost)

            def create_flag(side):
                path = Path("%s/gfx/flags/%s.tga" % (self.folder, this_battle[side]["country"]))
                if path.is_file():
                    flag = ImageQt(path)
                    flag = QPixmap.fromImage(flag).transformed(QTransform().rotate(90))
                    return flag
                else:
                    return QPixmap()
            self.defender_flag.setPixmap(create_flag("defender"))
            self.attacker_flag.setPixmap(create_flag("attacker"))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
preset_file, preset_folder = main.load_presets()
window.load_folder(preset_folder)
window.load_file(preset_file)
window.show()
app.exec()
