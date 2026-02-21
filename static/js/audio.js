window.SAMPLE_RATE = 8000; // 8kHz

function init_audio() {
  const ctx = new AudioContext({
    sampleRate: window.SAMPLE_RATE,
  });

  // this is a global variable
  window.play_chunk = function(float_arr) {
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
}
