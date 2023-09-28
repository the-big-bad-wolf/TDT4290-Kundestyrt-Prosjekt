import * as WebSocket from "ws";
import * as vscode from "vscode";

let statusBarItem: vscode.StatusBarItem;

export function setUp(context: vscode.ExtensionContext) {
  const ws = new WebSocket("ws://localhost:8080");

  statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  statusBarItem.text = "waiting for data";
  statusBarItem.show();

  ws.on("error", console.error);

  ws.on("open", function open() {
    ws.send("something");
  });

  ws.on("message", function message(data) {
    console.log("received: %s", data);

    let outputJson = JSON.parse(data.toString());

    statusBarItem.text =
      "cognitive load: " + outputJson["Current cognitive load"];

    context.subscriptions.push(statusBarItem);
  });
}
