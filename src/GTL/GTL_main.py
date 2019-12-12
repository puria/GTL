# -*- coding: utf-8 -*-

from GTL.GTL_params import font_name, out_path, txt_path
from GTL.typeface import Typeface


def main():
    typeface = Typeface(path=txt_path, family=font_name)
    typeface.render()
    typeface.save(out_path)
    print("DONE!")
    return 0


if __name__ == '__main__':
    main()
