import json
import os
from pathlib import Path
from GTL.GTL_params import width_ratio, fnt_baseline, style_name, fnt_dsc, fnt_xht, fnt_cap, fnt_asc, box_layout
import fontParts.world as fp
from GTL.glyph import Glyph


class Box(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h


class Typeface:
    UPM = 1000

    def __init__(self, path, family):
        self.path = Path(path)
        self.family = family
        self.fp = fp.NewFont(familyName=family, styleName=style_name)
        self.__setup()

    @property
    def glyph_names(self):
        return [g.name[:-5] for g in self.path.iterdir()]

    def get_glyph_metadata(self, glyph):
        filename = self.path / f"{glyph}.json"
        return json.loads(filename.read_text())

    def __setup(self):
        random_char = self.glyph_names[0]
        line_num = self.get_glyph_metadata(random_char)['lines']

        # Calculating box height
        box_height = int(self.UPM / line_num / 4) * 4

        # Calculating box width
        box_width = box_height * width_ratio

        # Calculating bottom line
        self.bottom = -box_height * fnt_baseline

        self.box = Box(box_width, box_height)
        self.box_layout = Box(box_layout[0], box_layout[1])
        self.fp.info.unitsPerEm = self.UPM
        self.fp.info.descender = - box_height * fnt_dsc
        self.fp.info.xHeight = box_height * fnt_xht
        self.fp.info.capHeight = box_height * fnt_cap
        self.fp.info.ascender = box_height * fnt_asc

    def __load_glyphs_from_path(self):
        return {g.name: json.loads(g.read_text()) for g in self.path.iterdir()}

    def save(self, out_path):
        self.fp.save(os.path.join(out_path, f'{self.family}.ufo'))

    def render(self):
        for glyph_name in self.glyph_names:
            glyph = Glyph(glyph_name, self)
            glyph.render()
