window.SAMPLE_RATE = 8000; // 8kHz

// ctx = audio context (this is set in init_audio)
let ctx = null;

function init_audio() {
  ctx = new AudioContext({
    sampleRate: window.SAMPLE_RATE,
  });
}

function play_chunk(float_arr) {
  const buf = new AudioBuffer({
    numberOfChannels: 1,
    length: float_arr.length,
    sampleRate: window.SAMPLE_RATE,
  });
  buf.getChannelData(0).set(float_arr);

  const src = ctx.createBufferSource(); // once a source has been played, it's no use anymore (can't replay), so we just throw it away
  src.buffer = buf;
  src.connect(ctx.destination);
  src.start();
  // we can set the onended if we want
  // src.onended = () => {};
}
