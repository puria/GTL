from GTL.GTL_syntax import syntax


class Cell:
    def __init__(self, glyph, l):
        self.glyph = glyph
        self.char = l['char']
        self.i = l['i']
        self.j = l['j']
        self.vertical_stretch = l.get('vertical_stretch', False)
        self.horizontal_stretch = l.get('horizontal_stretch', False)

    @property
    def width(self):
        box_w = self.glyph.tf.box.w
        return box_w / self.glyph.tf.box_layout.h

    @property
    def height(self):
        box_h = self.glyph.tf.box.h
        return box_h / self.glyph.tf.box_layout.w

    @staticmethod
    def from_list(glyph, lst):
        return [Cell(glyph, l) for l in lst]

    @staticmethod
    def first_by_position(i, j, lst):
        __ = [cell for cell in lst if cell.i == i and cell.j == j]
        return __[0] if __ else None

    def render(self, box_x, box_y):
        if self.char not in syntax.keys():
            print(f"There's an invalid character used ({self.char}) in glyph "
                  f"{self.glyph.name}.\n Please check glyph txt file or add "
                  f"the corresponding rule in the syntax.")
        else:
            # Starting point
            x = box_x + self.width / 2
            y = box_y + self.height / 2

            # Iterating over the cells
            for i in range(self.glyph.tf.box_layout.h):
                for j in range(self.glyph.tf.box_layout.w):
                    # Center of new cell
                    cell_x = x + j * self.width
                    cell_y = y + i * self.height

                    fn = syntax[self.char][0]
                    props = syntax[self.char][1]
                    fn(gly=self.glyph._glyph,
                       box=(cell_x, cell_y, self.width, self.height),
                       properties=props)

    def __str__(self):
        return f'Cell(i: {self.i}, j: {self.j}, char: {self.char})'