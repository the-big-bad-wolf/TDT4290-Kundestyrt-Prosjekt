// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import { setUp } from "./listener";
import * as fs from "fs";
import * as path from "path";
import { RawData } from "ws";

let statusBarItem: vscode.StatusBarItem;

let timeHelpPropmtWasActivated = new Date().getTime();
let timePausePropmtWasActivated = new Date().getTime();

// This method is called when your extension is activated
export function activate(context: vscode.ExtensionContext) {
  console.log("Congratulations, your extension is now active!");

  const disposable = vscode.commands.registerCommand(
    "extension.showData",
    () => {
      // The code you place here will be executed every time your command is executed
      // Display a message box to the user
      setUp();

      statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
      );
      statusBarItem.text = `Creating baseline $(loading~spin)`;
      statusBarItem.show();

      vscode.window.showInformationMessage(
        "Will now begin to create a baseline, just relax for a couple of minutes"
      );
    },
    context.subscriptions
  );

  context.subscriptions.push(statusBarItem);

  //logs code every five seconds
  setInterval(() => {
    const editor = vscode.window.activeTextEditor;
    const highlighted = editor!.document.getText();
    const now = new Date().toLocaleString();
    const data = `${now},\n${highlighted}\n`;

    //comment this out if you dont want to log everytime you activate the extension
    log(data);
  }, 5000);

  context.subscriptions.push(disposable);
}

export function updateStatusBarData(data: RawData) {
  /**
   * Updates the statusbar with the received data
   * @param {RawData} data - the data to be displayed in statusbar
   */

  let outputJson = JSON.parse(data.toString());

  statusBarItem.text =
    "cognitive load: " + outputJson["Current cognitive load"];
}

function log(data: string) {
  /**
   * Logs the code of the current open file to a csv file.
   * @param {string} data - the data to be logged
   */

  let today = new Date();

  let outputPath = path.join(
    __dirname,
    "../../vsCodeOutput/vscodeData-" +
      today.toISOString().slice(0, 10) +
      today.getHours() +
      today.getMinutes() +
      ".csv"
  );

  ensureDirectoryExistence(outputPath);

  try {
    fs.appendFileSync(outputPath, data + "\n\n");
  } catch (err) {
    console.error(err);
  }
}

function ensureDirectoryExistence(filePath: string) {
  /**
   * Checks if the filepath exists, if not it creates the necessary folders
   * @param {string} filePath - path to where you want to create a file
   */
  var dirname = path.dirname(filePath);
  if (fs.existsSync(dirname)) {
    return true;
  }
  ensureDirectoryExistence(dirname);
  fs.mkdirSync(dirname);
}

export async function offerHelpNotification() {
  /**
   * Creates a notification to user offering to turn on copilot
   */
  let now = new Date().getTime();

  //only prompt if it is five minutes since last promt
  if (now - timeHelpPropmtWasActivated > 5 * 60 * 1000) {
    timeHelpPropmtWasActivated = now;

    const selection = await vscode.window.showWarningMessage(
      "Do you want some help with that?",
      "Yes, please",
      "No, thank you"
    );

    if (selection === "Yes, please") {
      activateCopilotChat();
    } else if (selection === "No, thank you") {
      console.log("The user does not need help");
    }
  }
}

export function activateCopilotChat() {
  vscode.commands.executeCommand("github.copilot.interactiveEditor.explain");
}

export function pauseNotification() {
  /**
   * Creates a notification to the user telling them they should take a break
   */
  let now = new Date().getTime();

  //only prompt if five minutes since last prompt
  if (now - timePausePropmtWasActivated > 5 * 60 * 1000) {
    timePausePropmtWasActivated = now;
    vscode.window.showWarningMessage(
      "Hey there, you seem stressed. Maybe its time to take a break?"
    );
  }
}

// This method is called when your extension is deactivated
export function deactivate() {}
