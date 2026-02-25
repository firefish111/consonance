// check if WebSocketStream is supported
if (!("WebSocketStream" in self)) {
  // do everything in our power to break it, cause it won't work anyway
  alert("WebSocketStream is not available on this browser.\nPlease try on Chrome 124 or above.")
  document.body.innerHTML = "<h1>WebSocketStream not available on this browser.<br/>Please try on Chrome 124 or above.</h1>"
  throw "WebSocketStream not available."
  debugger;
}

async function play_sample(arraybuf) {
  // if halting we do nothing: neither play, nor wait
  if (halting) return null;

  // this is also async, so it does not block
//  const interval_id = put_canvas(arraybuf);
  canvas_buf = arraybuf;

  // call audio code.
  // this returns a promise that is resolved once the audio source ends,
  // and since all async functions return a promise, we can replace the promise with this one.
  // this is awaited later on
  return play_chunk(arraybuf);
}

async function pause_for(sample_n) {
  // if halting we do nothing: i.e. do not pause
  if (halting) return null;

  console.debug(`pausing for ${sample_n}`);
  return new Promise(r => // see play_sample() above for why we return
    setTimeout(
      r,
      sample_n * 1000 / window.SAMPLE_RATE
    )
  );
}

// handle tickets (i.e. non-binary JSON packets)
async function play_ticket(ticket) {
  console.debug(`received ticket ${JSON.stringify(ticket)}`);
  switch (ticket.type) {
    case "start":
      console.debug(`start: ${ticket}`);
      set_button(true);
      break;
    case "end":
      console.debug(`end: ${ticket}`);
      halting = false; // depause
      set_button(false);
//      clear_canvas();
      canvas_buf = null;
      break;
    case "error":
      console.debug(`error: ${ticket}`);
      alert(`Error: ${ticket.message}`);
      break;
    case "pause":
      await pause_for(ticket.samples);
      break;
    default:
      console.warn(`Unknown ticket type "${ticket.type}"`);
      break;
  }
}

// sets up websocket
async function init_ws() {
  // we do automatic detection of protocol (ws:// or wss://), we can't know if we have ssl or not
  const wss = new WebSocketStream(
    location.protocol.replace("http", "ws") + "//" +
    location.host +
    "/soundify" // url slug
  );

  console.log("Connected to", wss.url);

  const { readable, writable, extensions, protocol } = await wss.opened;

  console.log("Websocket open");

  const reader = readable.getReader();
  const writer = writable.getWriter();

  // reader generator: used so that reader and writer don't have to escape this scope
  async function* read_stream() {
    for (;;) {
      const { value, done } = await reader.read();

      if (done) return;
      yield value;
    }
  }

  // start infinite loop.
  // NOTE: we don't start this anywhere else because all of the above MUST BE COMPLETE
  // in order for this to work
  read_ws(read_stream);

  // this is a global variable so that writer doesn't have to escape scope
  window.send_ticket = function(ticket) {
    writer.write(JSON.stringify(ticket));
  }
}

// should run perpetually
async function read_ws(generator) {
  for await (const packet of generator()) {
    if (typeof packet == "string") { // if is a ticket
      console.debug("received", packet);
      const ticket = JSON.parse(packet);
      await play_ticket(ticket);
    } else { // if is a binary blob, i.e. list of samples
      const floated = new Float32Array(packet, 0, packet.byteLength >> 2); // this is just a pointer, does not copy
      await play_sample(floated);
    }
  }
}
