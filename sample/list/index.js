window.onload = setEmoji;

function setEmoji() {
  const emojiEnumElm = document.querySelector('#emojiEnum');

  let enumStr = '';
  sortedGlyphs = gGlyphs.sort(function (a, b) {
    if (a.codepoint > b.codepoint) {
      return 1;
    } else {
      return -1;
    }
  });
  // gGlyphs.forEach((glyphElm) => (enumStr += glyphElm.glyph));
  sortedGlyphs.forEach((glyphElm, index) => {
    // For debug
    if (index >= 20 * 5) {
      return;
    }

    enumStr += glyphElm.glyph;
    if ((index + 1) % 20 === 0) {
      enumStr += '<br>';
    }
  });
  emojiEnumElm.innerHTML = enumStr;
}
