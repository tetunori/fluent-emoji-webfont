from functools import partial
from json import loads
from operator import ne
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import parse, register_namespace, tostring
import subprocess
import codecs

subprocess.run('rm glyphs.txt', shell=True)

for glyph_dir in Path("fluentui-emoji/assets").iterdir():
    glyph_metadata_path = glyph_dir / "metadata.json"
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text(encoding="utf-8"))
    glyph: str = glyph_metadata["glyph"]
    codepoint: str = glyph_metadata["unicode"]
    print(f"{glyph},{codepoint}", file=codecs.open('glyphs.txt', 'a', 'utf-8'))
