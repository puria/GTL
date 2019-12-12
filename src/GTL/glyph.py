import json

from GTL.cell import Cell


class Glyph:
    def __init__(self, name, typeface):
        self.name = name
        self.tf = typeface
        self._glyph = self.tf.fp.newGlyph(self.name)
        self._glyph.unicode = hex(ord(name))[2:].zfill(4)
        self._glyph.clear()
        self.__load_metadata()
        self.__set_width()

    def __get_metadata(self):
        filename = self.tf.path / f"{self.name}.json"
        return json.loads(filename.read_text())

    def __load_metadata(self):
        metadata = self.__get_metadata()
        self.lines = metadata['lines']
        self.rows = metadata['rows']
        self.cells = Cell.from_list(self, metadata['cells'])

    def __set_width(self):
        self._glyph.width = self.tf.box.w * self.rows

    def render(self):
        box_x = 0
        box_y = self.tf.bottom # We start from the descender, then we go all the way up

        for line in reversed(range(self.lines)):
            for row in range(self.rows):
                cell = Cell.first_by_position(row, line, self.cells)
                cell.render(box_x, box_y)
                box_x += self.tf.box.w
            box_x = 0
            box_y += self.tf.box.h

