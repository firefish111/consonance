const out = document.querySelector("p");

// abstract behind a function so that we can return if things go awry
function init() {
  // check if WebSocketStream is supported
  if (!("WebSocketStream" in self)) {
    alert("WebSocketStream is not available on this browser.\nPlease try on Chrome 124 or above.")
    return;
  }

  // but we do automatic detection of protocol (ws:// or wss://), we can't know
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
    }
  }

  work();
}

init();
