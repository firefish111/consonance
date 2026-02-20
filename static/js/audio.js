window.SAMPLE_RATE = 8000; // 8kHz

let ctx = null;
let src = null;

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

  const src = ctx.createBufferSource();
  src.buffer = buf;
  src.connect(ctx.destination);
  src.start();
  src.onended = () => console.log("done");
}
