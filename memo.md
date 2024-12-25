
# Add submodule
Ref: https://ambiesoft.com/blog/archives/5962

```
git submodule add https://github.com/microsoft/fluentui-emoji.git
cd fluentui-emoji/
git checkout 14053d26005b9afe3ce0e020862ed5ab2335f989
```

# Build
```
$ source venv/bin/activate
bash: venv/bin/activate: No such file or directory
```
と怒られる。
Windowsの環境だと、`bin`ではなく`Scripts`なのでそのように修正
```
# source venv/bin/activate
source venv/Scripts/activate # For Windows
```

```
$ python -m prepare
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\tetun\Documents\GitHub\fluent-emoji-webfont\prepare.py", line 21, in <module>
    glyph_metadata: dict[str, Any] = loads(glyph_metadata_path.read_text())
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\pathlib.py", line 1059, in read_text 
    return f.read()
           ^^^^^^^^
UnicodeDecodeError: 'cp932' codec can't decode byte 0x87 in position 70: illegal multibyte sequence
```
と怒られる。multibyteが読めないとのことなので、
https://yamamon1010.hatenablog.jp/entry/pathlib_read_text_error
にあるように、`read_text`に`encoding="utf-8"`を付与
```
read_text(encoding="utf-8")
```

```
Removed incompatible mask from amphora_color (emoji_u1f3fa). Resulting SVG may look different.
Removed incompatible mask from amphora_color (emoji_u1f3fa). Resulting SVG may look different.
Removed incompatible mask from ballet_shoes_color (emoji_u1fa70). Resulting SVG may look different.
Removed incompatible mask from ballet_shoes_color (emoji_u1fa70). Resulting SVG may look different.
Removed incompatible mask from face_blowing_a_kiss_color (emoji_u1f618). Resulting SVG may look different.
Removed incompatible mask from grapes_color (emoji_u1f347). Resulting SVG may look different.
Removed incompatible mask from grapes_color (emoji_u1f347). Resulting SVG may look different.
Removed incompatible mask from grapes_color (emoji_u1f347). Resulting SVG may look different.
Removed incompatible mask from grapes_color (emoji_u1f347). Resulting SVG may look different.
Removed incompatible mask from grapes_color (emoji_u1f347). Resulting SVG may look different.
Removed incompatible mask from hamsa_color (emoji_u1faac). Resulting SVG may look different.
Removed incompatible mask from kissing_face_color (emoji_u1f617). Resulting SVG may look different.
Removed incompatible mask from kissing_face_with_closed_eyes_color (emoji_u1f61a). Resulting SVG may look different.
Removed incompatible mask from kissing_face_with_smiling_eyes_color (emoji_u1f619). Resulting SVG may look different.
Removed incompatible mask from kitchen_knife_color (emoji_u1f52a). Resulting SVG may look different.
Removed incompatible mask from lollipop_color (emoji_u1f36d). Resulting SVG may look different.
Removed incompatible mask from lollipop_color (emoji_u1f36d). Resulting SVG may look different.
Removed incompatible mask from melon_color (emoji_u1f348). Resulting SVG may look different.
Removed incompatible mask from snowman_without_snow_color (emoji_u26c4). Resulting SVG may look different.
Removed incompatible mask from snowman_without_snow_color (emoji_u26c4). Resulting SVG may look different.
Removed incompatible mask from strawberry_color (emoji_u1f353). Resulting SVG may look different.
Removed incompatible mask from tram_car_color (emoji_u1f68b). Resulting SVG may look different.
Removed incompatible mask from tram_car_color (emoji_u1f68b). Resulting SVG may look different.
Removed incompatible mask from tram_car_color (emoji_u1f68b). Resulting SVG may look different.
Removed incompatible mask from tram_car_color (emoji_u1f68b). Resulting SVG may look different.
```
とエラーは出ているが、終了はした。

```
$ git apply --directory venv/lib/*/site-packages/nanoemoji nanoemoji.patch
error: venv/lib/*/site-packages/nanoemoji/write_font.py: No such file or directory
```
libではなく、Libと思われる。

```
$ git apply --directory venv/Lib/*/site-packages/nanoemoji nanoemoji.patch
error: venv/Lib/*/site-packages/nanoemoji/write_font.py: No such file or directory
```

`*/` があると誤りっぽいので、直す。

```
$ nanoemoji --color_format glyf_colr_1 --family 'Fluent Color Emoji' --output_file FluentColorEmoji.ttf *.svg
bash: \Users\tetun\Documents\GitHub\fluent-emoji-webfont\venv/Scripts/nanoemoji: Argument list too long
```
リスト化した際のファイル数が多すぎるためであろうか。分割処理するように変更してみる。


