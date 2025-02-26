from pathlib import Path
import sys

from PIL.ImageQt import ImageQt
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap, QTransform

from victorialyser import assets, console


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path("%s/main.ui" % Path(__file__).parent), self)
        
        # Define attributes
        self.assets = dict()
        self.banners = dict()
        self.units = dict()
        self.folder = str()
        self.history = str()
        self.keys = list()
        self.tags = dict()
        self.wars = dict()
        self.battles = dict()
        self.belligerents = dict()
        self.war_goals = list()

        # Assign callbacks
        self.tag_edit.textChanged.connect(lambda: self.filter_list(self.tag_list, self.tag_edit))
        self.war_edit.textChanged.connect(lambda: self.filter_list(self.war_list, self.war_edit))
        self.battle_edit.textChanged.connect(lambda: self.filter_list(self.battle_list, self.battle_edit))
        self.tag_list.currentItemChanged.connect(self.select_tag)
        self.war_list.currentItemChanged.connect(self.select_war)
        self.battle_list.currentItemChanged.connect(self.select_battle)
        self.swap_btn.clicked.connect(self.nav)
        self.save_btn.clicked.connect(self.load_file)
        self.game_btn.clicked.connect(lambda: self.load_folder(False))

        # Hide windows
        self.statswidget.hide()

    def nav(self):
        if self.finwidget.isVisible():
            self.finwidget.hide()
            self.statswidget.show()
        else:
            self.finwidget.show()
            self.statswidget.hide()

    def load_file(self, file=None):
        if not file:
            file = str(QtWidgets.QFileDialog.getOpenFileName(self, "Select File")[0])
        if console.try_file(file):
            self.history, self.keys = console.read_file(file)
            self.tag_list.clear()
            self.tags = console.read_tags(self.folder, console.get_tags(self.history, self.keys))
            for tag in self.tags.keys():
                self.tag_list.addItem(tag)
            self.war_list.clear()
            self.wars = console.get_wars(self.history, self.keys)
            self.battle_list.clear()

    def load_folder(self, required, folder=None):
        if not folder:
            folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder"))
        if console.try_folder(folder):
            self.folder = folder
            self.assets = assets.get_assets(self.folder)
            self.main_bg.setPixmap(self.assets["main_bg"])
            self.fin_bg.setPixmap(self.assets["fin_bg"])
            self.stats_bg.setPixmap(self.assets["stats_bg"])
            self.swap_btn.setIcon(self.assets["swap_btn"])
            self.save_btn.setIcon(self.assets["save_btn"])
            self.game_btn.setIcon(self.assets["game_btn"])
            self.banners = {"land": {"won": self.assets["land_battle_won"], "lost": self.assets["land_battle_lost"]},
                            "naval": {"won": self.assets["naval_battle_won"], "lost": self.assets["naval_battle_lost"]}}
            self.units = {"land":[self.assets["cavalry"], self.assets["infantry"], self.assets["artillery"]],
                          "naval":[self.assets["heavy_ships"], self.assets["light_ships"], self.assets["transports"]]}
        elif folder != "":
            self.load_folder(required=required)
        else:
            if required:
                sys.exit(0)

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
                    belligerents, battles, war_goals = console.view_war(self.history, war, self.keys)
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
            self.belligerents, self.battles, self.war_goals = console.view_war(self.history, self.war_list.currentItem().text(), self.keys)
            battles = []
            for battle, data in self.battles.items():
                battles.append(battle)
            self.battle_list.clear()
            self.battle_list.addItems(battles)
            self.wargoals_lbl.setText(str(self.war_goals))

    def select_battle(self):
        if self.battle_list.currentItem() is None:
            pass
        else:
            # Assign alias
            this_battle = self.battles[self.battle_list.currentItem().text()]

            # Display name
            self.fin_lbl.setText("Battle of " + self.battle_list.currentItem().text())

            # Display leaders
            self.def_leader_lbl.setText(this_battle["defender"]["leader"])
            self.atk_leader_lbl.setText(this_battle["attacker"]["leader"])

            # Display winner
            for tag in self.tags:
                if self.tags[tag] == this_battle["attacker" if this_battle["result"] == "yes" else "defender"]["country"]:
                    self.win_lbl.setText("%s Won" % tag)

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
                    "attacker": self.atk_cav_fig,
                    "defender": self.def_cav_fig,
                    "unit_types": cavalry_types + heavy_ship_types
                },
                {
                    "attacker": self.atk_inf_fig,
                    "defender": self.def_inf_fig,
                    "unit_types": infantry_types + light_ship_types
                },
                {
                    "attacker": self.atk_art_fig,
                    "defender": self.def_art_fig,
                    "unit_types": artillery_types + transport_types
                }
            ]

            losses_labels = {
                "attacker": [self.atk_initial_fig, self.atk_casualties_fig, self.atk_survivors_fig],
                "defender": [self.def_initial_fig, self.def_casualties_fig, self.def_survivors_fig]
            }

            for s in ["attacker", "defender"]:
                for types in all_unit_types:
                    these_initial_units = sum_units(these_initial_units, types[s], s, types["unit_types"])
                losses_labels[s][0].setText(str(these_initial_units[s]))
                losses_labels[s][1].setText("-%s" % str(this_battle[s]["losses"]))
                losses_labels[s][2].setText(str(these_initial_units[s] - this_battle[s]["losses"]))

            # Display stack-wipe
            if self.def_casualties_fig.text() == "-0" and self.atk_casualties_fig.text() == "-0":
                if this_battle["result"] == "yes":
                    self.def_casualties_fig.setText("Stack Wipe")
                    self.def_survivors_fig.setText("0")
                else:
                    self.atk_casualties_fig.setText("Stack Wipe")
                    self.atk_survivors_fig.setText("0")

            # Display graphics
            terrain = "land"
            for unit_type in heavy_ship_types + light_ship_types + transport_types:
                if unit_type in this_battle["attacker"].keys() or unit_type in this_battle["defender"].keys():
                    terrain = "naval"
                    break

            self.banner_img.setPixmap(self.banners[terrain]["won" if this_battle["result"] == "yes" else "lost"])

            unit_geo = {"land":({'x':0, 'y':3}, {'x':0, 'y':35}, {'x':0, 'y':66}),
                        "naval":({'x':0, 'y':4}, {'x':0, 'y':37}, {'x':0, 'y':67})}
            for i, l in enumerate([self.def_units_lyt, self.atk_units_lyt]):
                for j, w in enumerate(l.children()):
                    w.setPixmap(self.units[terrain][j])
                    w.move(unit_geo[terrain][j]['x'] + (2*i if terrain == "land" else 3*i-1), unit_geo[terrain][j]['y'])

            def create_flag(side):
                path = Path("%s/gfx/flags/%s.tga" % (self.folder, this_battle[side]["country"]))
                if path.is_file():
                    return QPixmap.fromImage(ImageQt(path)).transformed(QTransform().rotate(90))
                else:
                    return QPixmap()

            self.def_flag_img.setPixmap(create_flag("defender"))
            self.atk_flag_img.setPixmap(create_flag("attacker"))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
preset_file, preset_folder = console.load_presets()
window.load_folder(True, preset_folder)
window.load_file(preset_file)
window.show()
app.exec()
