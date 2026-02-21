// check if WebSocketStream is supported
if (!("WebSocketStream" in self)) {
  // do everything in our power to break it, cause it won't work anyway
  alert("WebSocketStream is not available on this browser.\nPlease try on Chrome 124 or above.")
  document.body.innerHTML = "<h1>WebSocketStream not available on this browser.<br/>Please try on Chrome 124 or above.</h1>"
  throw "WebSocketStream not available."
  debugger;
}

// stub
async function play_sample(arraybuf) {
  // call audio code
  await play_chunk(arraybuf);

  // wait a while until we start to read the next one.
  // because all async functions return a promise, we can replace the promise with one
  // for waiting, which we will then await later on
  return new Promise(r =>
    setTimeout(
      r,
      arraybuf.length * 1000 / window.SAMPLE_RATE
    )
  );
}

// handle tickets (i.e. non-binary JSON packets)
async function play_ticket(ticket) {
  console.debug(`received ticket ${JSON.stringify(ticket)}`);
  switch (ticket.type) {
    case "start":
      console.debug(`start: ${ticket}`);
      set_button(false);
      break;
    case "end":
      console.debug(`end: ${ticket}`);
      set_button(true);
      break;
    case "error":
      console.debug(`error: ${ticket}`);
      alert(`Error: ${ticket.message}`);
      break;
    case "pause":
      console.debug(`pausing for ${ticket.samples}`);
      return new Promise(r => // see play_sample() above for why we return
        setTimeout(
          r,
          ticket.samples * 1000 / window.SAMPLE_RATE
        )
      );
    default:
      console.warn(`Unknown ticket type "${ticket.type}"`);
      break;
  }
}

let wss = null;
let reader = null;
let writer = null;

// sets up websocket
async function init_ws() {
  // we do automatic detection of protocol (ws:// or wss://), we can't know if we have ssl or not
  wss = new WebSocketStream(
    location.protocol.replace("http", "ws") + "//" +
    location.host +
    "/soundify" // url slug
  );

  console.log("Connected to", wss.url);

  const { readable, writable, extensions, protocol } = await wss.opened;

  console.log("Websocket open");

  reader = readable.getReader();
  writer = writable.getWriter();

  // start infinite loop.
  // NOTE: we don't start this anywhere else because all of the above MUST BE COMPLETE
  // in order for this to work
  read_ws();
}

// should run perpetually
async function read_ws() {
  for (;;) {
    const { value, done } = await reader.read();

    if (typeof value == "string") { // if is a ticket
      console.log(value);
      const ticket = JSON.parse(value);
      await play_ticket(ticket);
    } else { // if is a binary blob, i.e. list of samples
      const floated = new Float32Array(value, 0, value.byteLength >> 2); // this is just a pointer, does not copy
      await play_sample(floated);
    }

    if (done) break;
  }
}
