import sys
from functools import partial
from json import loads
from operator import ne
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import parse, register_namespace, tostring
import subprocess

def getCodePoint(glyph_dir: str):
    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))
    
    # Get the codepoint(s) for the emoji.
    codepoint: str = glyph_metadata["unicode"]
    codepoint = "_".join(filter(partial(ne, "fe0f"), codepoint.split(" ")))
    return codepoint

def isCodepointWorkAroundTarget(codePointText: str):
    targetList = ['🏃', '🏄', '🏊', '🏋', '🏌', '👮', '👰', '👱', '👳', '👷', '💁', '💂', '💆', '💇', '🕵', '🙅', '🙆', '🙇', '🙋', '🙍', '🙎', '🚣', '🚴', '🚵', '🚶', '🤦', '🤵', '🤷', '🤸', '🤹', '🤽', '🤾', '🦸', '🦹', '🧍', '🧎', '🧏', '🧖', '🧗', '🧘', '🧙', '🧚', '🧛', '🧜', '🧝', '🧞', '🧟', '🫃', '⛹']

    # to prevent each font file from getting too big.
    removeTargetList = ['🏃🏿‍➡️', '🏄🏿‍♂️', '🏊🏿‍♂️', '🏋🏿‍♂️', '🏌🏿‍♂️', '👮🏿‍♂️', '👰🏿‍♂️', '👱🏿‍♂️', '👳🏿‍♂️', '👷🏿‍♂️', '💁🏿‍♂️', '💂🏿‍♂️', '💆🏿‍♂️', '💇🏿‍♂️', '🕵🏿‍♂️', '🙅🏿‍♂️', '🙆🏿‍♂️', '🙇🏿‍♂️', '🙋🏿‍♂️', '🙍🏿‍♂️', '🙎🏿‍♂️', '🚣🏿‍♂️', '🚴🏿‍♂️', '🚵🏿‍♂️', '🚶🏿‍➡️', '🤦🏿‍♂️', '🤵🏿‍♂️', '🤷🏿‍♂️', '🤸🏿‍♂️', '🤹🏿‍♂️', '🤽🏿‍♂️', '🤾🏿‍♂️', '🦸🏿‍♂️', '🦹🏿‍♂️', '🧍🏿‍♂️', '🧎🏿‍➡️', '🧏🏿‍♂️', '🧖🏿‍♂️', '🧗🏿‍♂️', '🧘🏿‍♂️', '🧙🏿‍♂️', '🧚🏿‍♂️', '🧛🏿‍♂️', '🧜🏿‍♂️', '🧝🏿‍♂️', '🧞‍♂️', '🧟‍♂️', '🫄🏿', '⛹🏿‍♂️']

    for removeTarget in removeTargetList:
        removeTargetCodePointText = ''
        for removeTargetCP in removeTarget:
            removeTargetCodePointText += format(ord(removeTargetCP), 'x') + '_'
        removeTargetCodePointText = removeTargetCodePointText[:-len('_')]
        removeTargetCodePointText = removeTargetCodePointText.replace('_fe0f', '')
        # print(removeTargetCodePointText)
        if codePointText == removeTargetCodePointText:
            return False

    for target in targetList:
        targetCodePoint = format(ord(target), 'x')
        if targetCodePoint in codePointText:
            return True

    return False

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

# Replace target SVGs
replaceTargetSVGList = list(Path("replaceSVG").iterdir())
for svgFile in replaceTargetSVGList:
    print(f"find ./fluentui-emoji/ -name {svgFile.name}" )
    subprocess.run(f"find ./fluentui-emoji/ -name {svgFile.name} | xargs -I {{}} cp {str(svgFile)} {{}}", shell=True)

numGroup = 1
numElementsGroup = 0
gCodePoint = ''

pathList = list(Path("fluentui-emoji/assets").iterdir())
sortedPathList = sorted(pathList, key=getCodePoint)
prioritizedGlyphs = ["💻", "🔥", "🔬", "🗨️", "🚀", "🚒", "🟩", "🟫", "🦺", "🦼", "🦽", "↔️", "↕️", "☠️", "♀️", "♂️", "⚕️", "⚖️", "⚧️", "✈️", "❄️", "➡️", "⬛", "💼", "🔧", "🦯"]
prioritizedGlyphDirPathList = []

def makeGlyphMap(glyph_dir: str):
    global numGroup
    global numElementsGroup
    global gCodePoint

    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))

    # Get the codepoint(s) for the emoji.
    if "unicodeSkintones" not in glyph_metadata:
        # Emoji with no skin tone variations.
        codepoint: str = glyph_metadata["unicode"]
        codepoint = "_".join(filter(partial(ne, "fe0f"), codepoint.split(" ")))
        gCodePoint = codepoint
        # print(f"{fonttype}/*.svg")
        src_path = next(glyph_dir.glob(f"{fonttype}/*.svg"))
        glyph_map[src_path] = dest_dir / f"{numGroup:03}_{numElementsGroup:03}_emoji_u{codepoint}.svg"
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
            if fonttype == 'High Contrast':
                src_path = next(glyph_dir.glob(f"Default/{fonttype}/*.svg"))
                src_path = Path(f"HC{skintone}" + str(src_path))
            else:
                src_path = next(glyph_dir.glob(f"{skintone}/{fonttype}/*.svg"))
            glyph_map[src_path] = dest_dir / f"{numGroup:03}_{numElementsGroup:03}_emoji_u{codepoint}.svg"
            gCodePoint = codepoint
            numElementsGroup += 1
    if numElementsGroup > numElementsGroupCriteria:
        # continue as workaround
        if isCodepointWorkAroundTarget(gCodePoint):
            print(f"continue as workaround, {numGroup}, {numElementsGroup}")
        else:
            numGroup += 1
            numElementsGroup = 0

for glyph_dir in sortedPathList:
    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))

    prioritizedGlyphFound = False
    for prioritizedGlyph in prioritizedGlyphs:
        if glyph_metadata["glyph"] == prioritizedGlyph:
            prioritizedGlyphDirPathList.append(glyph_dir)
            prioritizedGlyphFound = True
    
    if prioritizedGlyphFound == True:
        continue

    makeGlyphMap(glyph_dir)

numGroup = 0
numElementsGroup = 0

for glyph_dir in prioritizedGlyphDirPathList:
    makeGlyphMap(glyph_dir)

# Remove incompatible <mask> elements from SVG files.
dest_dir.mkdir()
register_namespace("", "http://www.w3.org/2000/svg")
for src_path, dest_path in glyph_map.items():
    if fonttype in ['High Contrast', 'High Contrast Inverted']:
        for skintone in ["Default", "Light", "Medium-Light", "Medium", "Medium-Dark", "Dark"]:
          src_path_str = str(src_path)
          if skintone in src_path_str:
              src_path = src_path_str.replace(f"HC{skintone}fluentui-emoji", 'fluentui-emoji')
    tree = parse(src_path)
    # --- High Contrast Inverted: invert #RRGGBB colors ---
    if fonttype == 'High Contrast Inverted':
        def invert_hex_color(hex_color):
            if len(hex_color) == 7 and hex_color.startswith('#'):
                r = 255 - int(hex_color[1:3], 16)
                g = 255 - int(hex_color[3:5], 16)
                b = 255 - int(hex_color[5:7], 16)
                return '#{:02X}{:02X}{:02X}'.format(r, g, b)
            return hex_color
        for elem in tree.iter():
            for attr in elem.attrib:
                val = elem.attrib[attr]
                if isinstance(val, str) and val.startswith('#') and len(val) == 7:
                    elem.attrib[attr] = invert_hex_color(val)
    # --- end High Contrast Inverted ---
    for elem in tree.iter():
        for mask in elem.findall("{http://www.w3.org/2000/svg}mask"):
            elem.remove(mask)
            print(
                f"Removed incompatible mask from {src_path.stem} ({dest_path.stem})."
                " Resulting SVG may look different."
            )
    dest_path.write_text(tostring(tree.getroot(), encoding="unicode"))
