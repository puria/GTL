# -*- coding: utf-8 -*-

### MODULES
from GTL.GTL_syntax import syntax


### FUNCTIONS

# draw_bit_chr
# This function reads a character at a given position
# and creates a virtual box that gets divided into nxm (box_layout) cells.
# For each cell, a drawing function specified in the syntax dictionary gets executed.

# RGlyph, string, (float, float), (float, float), (int, int), dictionary
from GTL.set_unicode.set_unicode import set_unicode


def draw_bit_chr(gly, line, row, char, box, box_layout):

    if char['unicode'] in syntax.keys():

        # Unpacking
        box_x, box_y, box_w, box_h = box

        # Cell size
        cell_w = box_w/box_layout[1]
        cell_h = box_h/box_layout[0]

        # Starting point
        x = box_x + cell_w/2
        y = box_y + cell_h/2

        # Iteraring over the cells
        for i in range(box_layout[0]):
            for j in range(box_layout[1]):

                # Center of new cell
                cell_x = x + j*cell_w
                cell_y = y + i*cell_h

                function   = syntax[char][0]
                properties = syntax[char][1]

                function(gly = gly,
                         box = (cell_x, cell_y, cell_w, cell_h),
                         properties = properties)

    else:
        print(f"There's an invalid character used ({char}) in glyph {gly.name}. Please check glyph txt file or add the corresponding rule in the syntax.")



# draw_bit_lin
# This function iterates draw_bit_chr over a string (line) of characters.

# RGlyph, string, (float, float), (float, float), (int, int), dictionary
def draw_bit_lin(gly, line, gly_desc, box, box_layout):

    # Unpacking
    box_x, box_y, box_w, box_h = box

    for row in range(gly_desc['rows']):
        draw_bit_chr(gly, line, row, gly_desc, (box_x, box_y, box_w, box_h), box_layout)

        # Translating the x position by the width of the box
        box_x += box_w



# draw_bit_gly
# This function iterates draw_bit_lin over the full glyph ascii description.
# (So it draws the full glyph)

# RGlyph, list of lists, float, (float, float), (int, int), dictionary -> RGlyph
def draw_bit_gly(gly, gly_desc, dsc_hgt, box_size, box_layout):

    # Setting starting coordinates
    box_x = 0
    box_y = dsc_hgt    # We start from the descender, then we go all the way up

    # Iterating over glyph instructions (but backwards, so that we start from the descenders)
    for line in reversed(range(gly_desc['lines'])):
        draw_bit_lin(gly, line, gly_desc, (box_x, box_y, *box_size), box_layout)

        # Updating position once a row of characters (lin) is completed
        box_x = 0
        box_y += box_size[1]

    return gly


# draw_bit_fnt
# This function generates a full set of *alternative* (alt) glyphs from instructions.

# RFont, dictionary, string, float, (float, float), (int, int), dictionary -> RFont
def draw_bit_fnt(fnt, fnt_dict, dsc_hgt, box_size, box_layout):

    # Iterating over the dictionary (the instructions)
    for gly_name in fnt_dict.keys():

        # Creating new glyph
        gly = fnt.newGlyph(gly_name)
        set_unicode(gly)
        gly.clear()

        # Getting glyph description from dict
        gly_desc = fnt_dict[gly_name]

        # Setting glyph width
        gly.width = box_size[0] * gly_desc['rows']

        # Drawing the glyph
        draw_bit_gly(gly, gly_desc, dsc_hgt, box_size, box_layout)

    return fnt


def draw(typeface, glyphs, dsc_hgt, box_size, box_layout):
    return draw_bit_fnt(typeface, glyphs, dsc_hgt, box_size, box_layout)