// check if WebSocketStream is supported
if (!("WebSocketStream" in self)) {
  alert("WebSocketStream is not available on this browser.\nPlease try on Chrome 124 or above.")
  throw "WebSocketStream not available."
  debugger;
}

// stub
async function play_sample(arraybuf) {
  await play_chunk(arraybuf);
  return new Promise(r =>
    setTimeout(
      r,
      arraybuf.length * 1000 / window.SAMPLE_RATE
    )
  );
}

async function play_ticket(ticket) {
  console.log(`received ticket ${JSON.stringify(ticket)}`);
  switch (ticket.type) {
    case "start":
      console.log(`start: ${ticket}`);
      set_button(false);
      break;
    case "end":
      console.log(`end: ${ticket}`);
      set_button(true);
      break;
    case "error":
      console.log(`end: ${ticket}`);
      alert(`Error: ${ticket.message}`);
      break;
    case "pause":
      console.log(`pausing for ${ticket.samples}`);
      return new Promise(r =>
        setTimeout(
          r,
          ticket.samples * 1000 / window.SAMPLE_RATE
        )
      );
    default:
      break;
  }
}

let wss = null;
let reader = null;
let writer = null;

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

  read_ws();
}

// should run perpetually
async function read_ws() {
  for (;;) {
    const { value, done } = await reader.read();

    if (typeof value == "string") { // if is a ticket
      const ticket = JSON.parse(value);
      await play_ticket(JSON.parse(value));
    } else { // if is a binary blob, i.e. list of samples
      const floated = new Float32Array(value, 0, value.byteLength >> 2); // this is just a pointer, does not copy
      await play_sample(floated);
    }

    if (done) break;
  }
}
