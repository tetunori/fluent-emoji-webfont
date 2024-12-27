# Fluent Emoji Webfont🤗
Version 0.8.0  
⭐KeyVisual  
You can confirm from a [sample demo](https://tetunori.github.io/fluent-emoji-webfont/sample/list/).

# Description🖊️
This repository supplies Webfont version of [`Fluent Emoji`](https://github.com/microsoft/fluentui-emoji) from Microsoft.  
By using this, You can use `Fluent Emoji` anywhere/anytime with any device(even with a non-Windows device)!  
Here you can choose three types of `Fluent Emoji`.
- `Fluent Emoji Color`
- `Fluent Emoji Flat`
- `Fluent Emoji High Contrast`

# Samples
- [p5.js demo](https://tetunori.github.io/fluent-emoji-webfont/sample/p5.js_usage)
- [Listing emoji](https://tetunori.github.io/fluent-emoji-webfont/sample/list)

⭐Vis

# How to use🪄
## General usage
Add `@import url('***.css')` and `font-family` in your `.css` file as below:

```css
@import url('https://tetunori.github.io/fluent-emoji-webfont/dist/FluentEmojiColor.css');

html, body {
  ...
  font-family: 'Fluent Emoji Color';
  ...
}
```

Here are the other options for `font-family`:
```css
@import url('https://tetunori.github.io/fluent-emoji-webfont/dist/FluentEmojiFlat.css');
...
  font-family: 'Fluent Emoji Flat';
```
```css
@import url('https://tetunori.github.io/fluent-emoji-webfont/dist/FluentEmojiHighContrast.css');
...
  font-family: 'Fluent Emoji High Contrast';
```

## p5.js usage
After `@import url('***.css')` in `.css` file, call `textFont()` as below:
```javascript
function setup() {
  createCanvas(windowWidth, windowHeight);
  textFont('Fluent Emoji Color');
}

function draw() {
  background(0)
  text('🐲🥳🎉👏🎊🍻', width / 2, height / 2);
}
```

# Issues
- Currently, Some fonts cannot be displayed. Perhaps the `unicode-range` specification in `css` file is not working.
- Some artworks in `Color` fonts are slightly different from the original ones. It might depends on the font/svg conversion tool. 

# Maintenance
## Build
Execute `build.sh` with an `fontType` option.
```bash
./build.sh color
```
* Options: `color`, `flat` and `hc` for `High Contrast`

Then, you can get `FluentEmoji***NNN.woff2` files and a `FluentEmoji***.css` file after long (about half an hour) time build.

## Test/Confirm
Check the result with the [Listing emoji](https://tetunori.github.io/fluent-emoji-webfont/sample/list) sample.


# License⚖️
Copyright (c) 2024 [Tetsunori Nakayama](https://github.com/tetunori). MIT License.

# Author🧙‍♂️
Tetsunori Nakayama

# References📚
## fluentui-emoji
[fluentui-emoji](https://github.com/microsoft/fluentui-emoji) by [microsoft](https://github.com/microsoft). MIT License.

## fluent-color-emoji
[fluent-color-emoji](https://github.com/GCMarvin/fluent-color-emoji) by [GCMarvin](https://github.com/GCMarvin). The Unlicense.

## p5.js
[p5.js](https://github.com/processing/p5.js) by [Processing Foundation](https://github.com/processing). GNU Lesser General Public License v2.1.

