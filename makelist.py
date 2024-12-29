from functools import partial
from json import loads
from operator import ne
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import parse, register_namespace, tostring
import subprocess
import codecs

def getCodePoint(glyph_dir: str):
    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))
    
    # Get the codepoint(s) for the emoji.
    codepoint: str = glyph_metadata["unicode"]
    codepoint = "_".join(filter(partial(ne, "fe0f"), codepoint.split(" ")))
    return codepoint

subprocess.run('rm glyphs.js', shell=True)
print(f"const gGlyphs = [", file=codecs.open('glyphs.js', 'a', 'utf-8'))

pathList = list(Path("fluentui-emoji/assets").iterdir())
sortedPathList = sorted(pathList, key=getCodePoint)

for glyph_dir in sortedPathList:
    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))

    if "unicodeSkintones" not in glyph_metadata:
        # Emoji with no skin tone variations.
        glyph: str = glyph_metadata["glyph"]
        codepoint: str = glyph_metadata["unicode"]
        print(f"  {{glyph: '{glyph}', codepoint: '{codepoint}'}},", file=codecs.open('glyphs.js', 'a', 'utf-8'))
    else:
        # Emoji with skin tone variations.
        var_metadata: list[str] = glyph_metadata["unicodeSkintones"]
        for codepoint in var_metadata:
            codepointElements: list[str] = codepoint.split(" ")
            glyph = ''
            for codepointElement in codepointElements:
              glyph += chr(int(codepointElement,16))
            print(f"  {{glyph: '{glyph}', codepoint: '{codepoint}'}},", file=codecs.open('glyphs.js', 'a', 'utf-8'))
    
print(f"];", file=codecs.open('glyphs.js', 'a', 'utf-8'))

subprocess.run('mv glyphs.js sample/list/', shell=True)
