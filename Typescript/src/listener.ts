import * as WebSocket from "ws";

export function setUp() {
  const ws = new WebSocket("ws://localhost:8080");

  ws.on("error", console.error);

  ws.on("open", function open() {
    ws.send("something");
  });

  ws.on("message", function message(data) {
    console.log("received: %s", data);
  });
}
