# -*- coding: utf-8 -*-
import json
from pathlib import Path

import click
from GTL.typeface import Typeface


@click.group()
def cli():
    pass


@cli.command(help="Creates a new typeface project")
@click.argument('project_name', required=True, type=str)
@click.option('-p', '--glyph-path', prompt="Insert the folder where all your glyphs are stored", type=Path)
@click.option('--style', prompt=True, type=click.Choice(['Regular', 'Bold', 'Rectangular', 'Dizzy']), default="Regular")
@click.option('--baseline', prompt="Set baseline row (counting from bottom of txt)", default=3, type=int)
@click.option('--x-height', prompt="Set font x-height (number of rows)", type=int, default=6)
@click.option('--font-cap', prompt="Set font capital height (number of rows)", type=int, default=8)
@click.option('--font-asc', prompt="Set font ascender height (number of rows)", type=int, default=10)
@click.option('--font-dsc', prompt="Set font descender height (number of rows)", type=int, default=2)
@click.option('--ratio', prompt="Set box width ratio (width_ratio = 1 for square proportions)", type=float, default=1)
@click.option('--box-layout-width', prompt="Set box layout width", type=int, default=1)
@click.option('--box-layout-height', prompt="Set box layout height", type=int, default=1)
def create(project_name, glyph_path, style, baseline, x_height, font_cap, font_asc, font_dsc, ratio,
           box_layout_width, box_layout_height):
    p = Path(project_name)
    p.mkdir(parents=True, exist_ok=True)

    config_dict = {
        "txt_path": str(glyph_path.resolve()),
        "font_name": project_name,
        "style_name": style,
        "fnt_baseline": baseline,
        "fnt_xht": x_height,
        "fnt_cap": font_cap,
        "fnt_asc": font_asc,
        "fnt_dsc": font_dsc,
        "width_ratio": ratio,
        "box_layout_width": box_layout_width,
        "box_layout_height": box_layout_height,
    }

    config = p / "config.json"
    with config.open("w", encoding="utf-8") as f:
        f.write(json.dumps(config_dict, indent=2))
    click.secho("DONE", fg='green')


@cli.command(help="Generates the .ufo file, from a project directory")
@click.argument('output_dir', type=click.Path(exists=True))
@click.option('--config', type=Path, default="config.json")
def compile(output_dir, config):
    parsed_config = json.loads(config.read_text())
    typeface = Typeface(config=parsed_config)
    typeface.render()
    typeface.save(output_dir)
    print("OK")
    return 0


if __name__ == '__main__':
    cli()
