from functools import partial
from json import loads
from operator import ne
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import parse, register_namespace, tostring
import subprocess
import codecs

subprocess.run('rm glyphs.js', shell=True)
print(f"const gGlyphs = [", file=codecs.open('glyphs.js', 'a', 'utf-8'))

for glyph_dir in Path("fluentui-emoji/assets").iterdir():
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

