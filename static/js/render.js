const canv = document.querySelector("canvas");
const rend = canv.getContext("2d");

// NOTE: there is always guaranteed to be 400 samples, as there is a minimum of 0.05 seconds per sound, and 8000 samples per second. If this gets cut short, something is wrong anyway, so behaviour is undefined
const N_SAMPLES = 400;

// oscilloscope path
async function clear_canvas() {
  rend.clearRect(0, 0, canv.width, canv.height);
}

clear_canvas();

const COLOURS = ["#f04b35", "#59de37", "#0bc2db", "#ff4ccf"];

// 1/2 * cos^2(pi*t) + 1/2
const scale = t => (Math.cos(Math.PI*t)**2)*.5 + 0.5

let t = 0;

let canvas_buf = null;
let colour_n = 0;

async function set_buf(buffer) {
  canvas_buf = buffer;
  let hue = Math.trunc(Math.random() * COLOURS.length);
}

async function cycle_hue() {
  colour_n++;
  colour_n %= COLOURS.length;
}

setInterval(() => {
  // baseline x
  const baseline = canv.height / 2;
  const y_segment = canv.width / N_SAMPLES;

  clear_canvas();

  rend.beginPath();
  rend.moveTo(canv.width, baseline);
  rend.strokeStyle = "#666666";
  rend.lineTo(0, baseline);
  rend.stroke();

  // already at beginning from above

  if (canvas_buf) {
    const size = document.querySelector("input#time_per_syllable").value / 0.05;

    rend.beginPath();
    rend.strokeStyle = COLOURS[colour_n];
    for (let i = 0; i < N_SAMPLES; ++i) {
      rend.lineTo(i * (y_segment + 1), (canvas_buf[i] * scale(t/size)) * baseline + baseline);
    }
    rend.stroke();
  }

  t++;
}, 50); // every 50 ms
