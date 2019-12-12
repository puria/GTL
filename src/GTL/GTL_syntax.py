# -*- coding: utf-8 -*-


### CONSTANTS
from GTL.shape_functions.do_nothing import do_nothing
from GTL.shape_functions.rectangle import rectangle

ORIENTATIONS = ["NW", "NE", "SW", "SE"]






### PROPERTIES

# Examples below

# p_do_nothing = {
#     }


rectangle_props = {
    "scale_x": 1,
    "scale_y": 1,
    "rotation": 0
}


# p_ellipse = {
#     "scale_x": 1,
#     "scale_y": 1,
#     "rotation": 0,
#     "squaring": .56
#     }


# p_ellipse_quarter = {
#     "scale_x": 1,
#     "scale_y": 1,
#     "rotation": 0,
#     "squaring": .56,
#     "orientation": "NE"
# }


# p_rhombus = {
#     "scale_x": 1,
#     "scale_y": 1,
#     "rotation": 0,
#     "squaring": 0
#     }


# p_triangle = {
#     "scale_x": 1,
#     "scale_y": 1,
#     "rotation": 0,
#     "squaring": 0,
#     "orientation": "NE",
# }


# p_random_function = {
#     "function_properties_list": [(rectangle      , p_rectangle      ),
#                                  (ellipse        , p_ellipse        ),
#                                  (ellipse_quarter, p_ellipse_quarter),
#                                  (ellipse        , p_rhombus        ),
#                                  (ellipse_quarter, p_triangle       )
#                                 ]
# }





### SYNTAX

syntax = {
    "·": (do_nothing, {}),
    "│": (rectangle, rectangle_props)
}