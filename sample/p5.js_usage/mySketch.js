function setup() {
  createCanvas(windowWidth, windowHeight);
  textSize(width / 10);
  textAlign(CENTER, CENTER);

  // Set `Fluent Color Emoji` font here.
  textFont('fluentcoloremoji');
}

function draw() {
  background(20);
  text('🐲🥳🎉👏🎊🍻', width / 2, height / 3);
  text('🎁🦌🎅🔔🎄🌟', width / 2, (2 * height) / 3);
}
