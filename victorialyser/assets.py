from pathlib import Path

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QIcon, QPixmap


def _draw_units(image, rect, seeds, plant=(0, 0, 0, 0)):
    image = Image.open(image).convert("RGBA")
    for seed in seeds:
        ImageDraw.floodfill(image, seed, plant, thresh=50)
    return QPixmap.fromImage(ImageQt(image)).copy(rect)


def get_assets(folder):
    assets = dict()

    # Icons
    assets["button"] = QIcon(QPixmap.fromImage(ImageQt(Path("%s/gfx/interface/diplo_addtowar.dds" % folder))))

    # Pixmaps
    assets["main_bg"] = QPixmap.fromImage(ImageQt(Path("%s/gfx/interface/frontend_ms_bg.dds" % folder)))
    assets["fin_bg"] = QPixmap.fromImage(ImageQt(Path("%s/gfx/interface/combat_end_bg.dds" % folder)))
    assets["land_battle_won"] = QPixmap.fromImage(ImageQt(Path("%s/gfx/interface/combat_end_land_won.dds" % folder)))
    assets["land_battle_lost"] = QPixmap.fromImage(ImageQt(Path("%s/gfx/interface/combat_end_land_lost.dds" % folder)))
    assets["naval_battle_won"] = QPixmap.fromImage(ImageQt(Path("%s/gfx/interface/combat_end_naval_won.dds" % folder)))
    assets["naval_battle_lost"] = QPixmap.fromImage(ImageQt(Path("%s/gfx/interface/combat_end_naval_lost.dds" % folder)))

    # Units
    assets["cavalry"] = _draw_units(Path("%s/gfx/interface/unit_folder_army_2_cavalry.dds" % folder),
                          QRect(37, 4, 28, 28), [(37, 4), (37, 34), (64, 4)])
    assets["infantry"] = _draw_units(Path("%s/gfx/interface/unit_folder_army_1_infantry.dds" % folder),
                           QRect(37, 4, 28, 28), [(37, 4), (37, 34), (64, 4), (47, 4)])
    assets["artillery"] = _draw_units(Path("%s/gfx/interface/unit_folder_army_3_artillery.dds" % folder),
                            QRect(37, 4, 28, 28), [(37, 4), (37, 34)])
    assets["heavy_ships"] = _draw_units(Path("%s/gfx/interface/unit_folder_navy_2_manowar.dds" % folder),
                              QRect(41, 4, 32, 28), [(41, 4), (41, 34), (72, 4)])
    assets["light_ships"] = _draw_units(Path("%s/gfx/interface/unit_folder_navy_1_frigate.dds" % folder),
                              QRect(41, 4, 32, 28), [(41, 4), (41, 34)])
    assets["transports"] = _draw_units(Path("%s/gfx/interface/unit_folder_navy_0_clipper_transport.dds" % folder),
                             QRect(41, 4, 32, 28), [(41, 4), (41, 34)])

    return assets
