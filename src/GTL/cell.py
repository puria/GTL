import ast

from GTL.shapes import rect, diag_0, diag_1


class Cell:
    def __init__(self, glyph, l):
        self.glyph = glyph
        self.char = l['char']
        self.i = l['i']
        self.j = l['j']
        self.vertical_stretch = l.get('vertical_stretch', False)
        self.horizontal_stretch = l.get('horizontal_stretch', False)
        transformation = l.get('transformation', None)
        self.structure = ast.literal_eval(transformation.get('structure', None)) if transformation else None
        self.index = transformation.get('index', None) if transformation else None

    @property
    def width(self):
        box_w = self.glyph.tf.box.w
        return box_w / self.glyph.tf.box_layout.h

    @property
    def height(self):
        box_h = self.glyph.tf.box.h
        return box_h / self.glyph.tf.box_layout.w

    def get_transformations(self):
        functions = {
            'rect': rect,
            'diag_0': diag_0,
            'diag_1': diag_1,
        }

        if not self.structure:
            return {}

        return { functions[__[0]]: (__[1], __[2]) for __ in self.structure }


    @staticmethod
    def from_list(glyph, lst):
        return [Cell(glyph, l) for l in lst]

    @staticmethod
    def first_by_position(i, j, lst):
        __ = [cell for cell in lst if cell.i == i and cell.j == j]
        return __[0] if __ else None

    def render(self, box_x, box_y):
        # Starting point
        x = box_x + self.width / 2
        y = box_y + self.height / 2

        # Iterating over the cells
        for i in range(self.glyph.tf.box_layout.h):
            for j in range(self.glyph.tf.box_layout.w):
                # Center of new cell
                cell_x = x + j * self.width
                cell_y = y + i * self.height
                box = (cell_x, cell_y, self.width, self.height)

                for fn, params in self.get_transformations().items():
                    fn(self.glyph._glyph, box, params[0], params[1], tck=30)

    def __str__(self):
        return f'Cell(i: {self.i}, j: {self.j}, char: {self.char})'