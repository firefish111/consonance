// check if WebSocketStream is supported
if (!("WebSocketStream" in self)) {
  alert("WebSocketStream is not available on this browser.\nPlease try on Chrome 124 or above.")
  throw "WebSocketStream not available."
  debugger;
}

// WORKING CODE
const out = document.querySelector("p");

// stub
async function play_sample(arraybuf) {
  console.log(`received sample ${arraybuf}`);
  await new Promise(r => setTimeout(r, arraybuf.length/8));
}

async function play_ticket(ticket) {
  console.log(`received ticket ${ticket}`);
  await new Promise(r => setTimeout(r, ticket.pause_samples/8));
}

// we do automatic detection of protocol (ws:// or wss://), we can't know if we have ssl or not
const wss = new WebSocketStream(
  location.protocol.replace("http", "ws") + "//" +
  location.host +
  "/soundify" // url slug
);

console.log("Connected to", wss.url);

async function work() {
  const { readable, writable, extensions, protocol } = await wss.opened;

  console.log("Websocket open");

  const reader = readable.getReader();
  const writer = writable.getWriter();

  // TODO: write on button press
  writer.write("blah blah blah");

  for (;;) {
    const { value, done } = await reader.read();
    console.log(value, done);

    if (typeof value == "string") { // if is a ticket
      const ticket = JSON.parse(value);
      if (ticket.type == "initial") {
        // TODO: initial ticket handling
        console.log(`do something with this idk: ${ticket}`);
      } else {
        await play_ticket(JSON.parse(value));
      }
    } else { // if is a binary blob, i.e. list of samples
      const floated = new Float32Array(value, 0, value.byteLength >> 2); // this is just a pointer, does not copy
      await play_sample(floated);
    }

    if (done) break;
  }
}

work();
