import sys
from functools import partial
from json import loads
from operator import ne
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import parse, register_namespace, tostring

def getCodePoint(glyph_dir: str):
    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))
    
    # Get the codepoint(s) for the emoji.
    codepoint: str = glyph_metadata["unicode"]
    codepoint = "_".join(filter(partial(ne, "fe0f"), codepoint.split(" ")))
    return codepoint

args = sys.argv
fonttype = args[1]
dest_dir = Path("build")
glyph_map: dict[Path, Path] = {}
numElementsGroupCriteria = 20

skintone_map = {
    "1f3fb": "Light",
    "1f3fc": "Medium-Light",
    "1f3fd": "Medium",
    "1f3fe": "Medium-Dark",
    "1f3ff": "Dark",
}

numGroup = 1
numElementsGroup = 0

pathList = list(Path("fluentui-emoji/assets").iterdir())
sortedPathList = sorted(pathList, key=getCodePoint)

for glyph_dir in sortedPathList:
    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))
    
    # Get the codepoint(s) for the emoji.
    if "unicodeSkintones" not in glyph_metadata:
        # Emoji with no skin tone variations.
        codepoint: str = glyph_metadata["unicode"]
        codepoint = "_".join(filter(partial(ne, "fe0f"), codepoint.split(" ")))
        # print(f"{fonttype}/*.svg")
        src_path = next(glyph_dir.glob(f"{fonttype}/*.svg"))
        glyph_map[src_path] = dest_dir / f"{numGroup:03}_{numElementsGroup:02}_emoji_u{codepoint}.svg"
        numElementsGroup += 1
    else:
        if fonttype == 'High Contrast':
            codepoint: str = glyph_metadata["unicode"]
            codepoint = "_".join(filter(partial(ne, "fe0f"), codepoint.split(" ")))
            src_path = next(glyph_dir.glob(f"Default/{fonttype}/*.svg"))
            glyph_map[src_path] = dest_dir / f"{numGroup:03}_{numElementsGroup:02}_emoji_u{codepoint}.svg"
            numElementsGroup += 1
        else:
            # Emoji with skin tone variations.
            var_metadata: list[str] = glyph_metadata["unicodeSkintones"]
            for codepoint in var_metadata:
                codepoint = "_".join(filter(partial(ne, "fe0f"), codepoint.split(" ")))
                skintone = (
                    skintone_map.get(codepoint.split("_")[1], "Default")
                    if "_" in codepoint
                    else "Default"
                )
                src_path = next(glyph_dir.glob(f"{skintone}/{fonttype}/*.svg"))
                glyph_map[src_path] = dest_dir / f"{numGroup:03}_{numElementsGroup:02}_emoji_u{codepoint}.svg"
                numElementsGroup += 1
    if numElementsGroup > numElementsGroupCriteria:
        numGroup += 1
        numElementsGroup = 0

# Remove incompatible <mask> elements from SVG files.
dest_dir.mkdir()
register_namespace("", "http://www.w3.org/2000/svg")
for src_path, dest_path in glyph_map.items():
    tree = parse(src_path)
    for elem in tree.iter():
        for mask in elem.findall("{http://www.w3.org/2000/svg}mask"):
            elem.remove(mask)
            print(
                f"Removed incompatible mask from {src_path.stem} ({dest_path.stem})."
                " Resulting SVG may look different."
            )
    dest_path.write_text(tostring(tree.getroot(), encoding="unicode"))
