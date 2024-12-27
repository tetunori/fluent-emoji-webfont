const setEmoji = () => {
  const emojiEnumElm = document.querySelector('#emojiEnum');

  let enumStr = '';
  sortedGlyphs = gGlyphs.sort(function (a, b) {
    if (a.codepoint > b.codepoint) {
      return 1;
    } else {
      return -1;
    }
  });

  sortedGlyphs.forEach((glyphElm, index) => {
    // For debug
    if (index >= 20 * 5) {
      return;
    }

    enumStr += glyphElm.glyph;
    if ((index + 1) % 10 === 0) {
      enumStr += '<br>';
    }
  });
  emojiEnumElm.innerHTML = enumStr;
}

const radio_func = () => {
  let elements = document.getElementsByName('fontType');
  let len = elements.length;

  for (let i = 0; i < len; i++) {
    if (elements.item(i).checked) {
      setFontFamily(elements.item(i).value);
    }
  }
}

const setFontFamily = (value) => {
  let fontFamilyText = 'sans-serif';

  switch (value) {
    case 'color':
      fontFamilyText = 'Fluent Emoji Color';
      break;
    case 'flat':
      fontFamilyText = 'Fluent Emoji Flat';
      break;
    case 'highContrast':
      fontFamilyText = 'Fluent Emoji High Contrast';
      break;
    case 'none':
    default:
      break;
  }

  document.body.style.fontFamily = fontFamilyText;
};

window.onload = setEmoji;
