import * as WebSocket from "ws";
import {
  offerHelpNotification,
  initializeHelpButton,
  pauseNotification,
} from "./extension";

export function setUp() {
  let initialMessage = true;

  const ws = new WebSocket("ws://localhost:8080");

  ws.on("error", console.error);

  ws.on("open", function open() {
    ws.send("something");
  });

  ws.on("message", function message(data) {
    if (initialMessage) {
      initialMessage = false;
      initializeHelpButton();
    }

    console.log("received: %s", data);

    let JSONData = JSON.parse(data.toString());

    if (JSONData["Need help"] == "True") {
      offerHelpNotification();
    }

    /*if (JSONData["Is stressed"] == "True") {
      offerPauseNotification()
    }*/
  });
}
