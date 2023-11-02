import * as WebSocket from "ws";
import {
  offerHelpNotification,
  initializeHelpButton,
  pauseNotification,
  updateStatusBarData,
} from "./extension";

export function setUp(AIInitiateHelp: boolean) {
  /**
   * The setup of the websocket
   * @param {boolean} AIInitiateHelp - tells the websocket if it should use the AI initiated help or not
   */

  let initialMessage = true;

  const ws = new WebSocket("ws://localhost:8080");

  ws.on("error", console.error);

  ws.on('open', function open() {
    ws.send("something"); // Make sure this is a string
  });

  ws.on("message", function message(data) {
    if (initialMessage && !AIInitiateHelp) {
      initialMessage = false;
      initializeHelpButton();
    }

    console.log("received: %s", data);

    if (AIInitiateHelp) {
      updateStatusBarData(data);

      let JSONData = JSON.parse(data.toString());

      if (JSONData["Need help"] == "True") {
        offerHelpNotification();
      }

      /*if (JSONData["Is stressed"] == "True") {
      offerPauseNotification()
      }*/
    }
  });
}
