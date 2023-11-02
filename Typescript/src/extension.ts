import * as vscode from "vscode";
import { setUp } from "./listener";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { RawData } from "ws";

let statusBarItem: vscode.StatusBarItem;

let timeHelpPropmtWasActivated = new Date().getTime();
let timePausePropmtWasActivated = new Date().getTime();

export function activate(context: vscode.ExtensionContext) {
  /**
   * Function that is called when the extension is activated
   * @param {vscode.ExtensionContext} context - the context of the extension
   */

  console.log("Congratulations, your extension is now active!");

  const AIInitiatedHelp = vscode.commands.registerCommand(
    "extension.AIInitiatedHelp",
    () => {
      //call the setup of the websocket telling it that it should use the AI initiated help,
      //and set up the statusbar
      setUp(true);
      setUpStatusbar();
      log();
    },
    context.subscriptions
  );

  const UserInitiatedHelp = vscode.commands.registerCommand(
    "extension.UserInitiatedHelp",
    () => {
      //call the setup of the websocket telling it that it should not use the AI initiated help,
      //and set up the statusbar
      setUp(false);
      setUpStatusbar();
      log();
    },
    context.subscriptions
  );

  context.subscriptions.push(statusBarItem);
  context.subscriptions.push(AIInitiatedHelp);
  context.subscriptions.push(UserInitiatedHelp);
}

export function initializeHelpButton() {
  /**
   * Creates a button in the bottom right corner of the screen
   * that will open the copilot chat when clicked
   */

  statusBarItem.text = `Help me!`;

  const helpCommand = "extension.help";
  vscode.commands.registerCommand(helpCommand, () => {
    activateCopilotChat();
  });

  //set the command for the button
  statusBarItem.command = helpCommand;
}

function setUpStatusbar() {
  /**
   * Set up the initial statusbar that is displayed during the creation of the baseline
   */

  statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  statusBarItem.text = `Creating baseline $(loading~spin)`;
  statusBarItem.show();

  vscode.window.showInformationMessage(
    "Will now begin to create a baseline, just relax for a couple of minutes"
  );
}

export function updateStatusBarData(data: RawData) {
  /**
   * updates the statusbar with the received data
   * @param {RawData} data - the data to be displayed in statusbar
   */

  let outputJson = JSON.parse(data.toString());

  statusBarItem.text =
    "cognitive load: " + outputJson["Current cognitive load"];
}

function log() {
  /**
   * Logs the code of the current open file to a csv file.
   */

  //create file path to the desktop where the data will be logged
  let today = new Date();
  const dir = path.join(os.homedir(), "Desktop");
  let outputPath = path.join(
    dir,
    "vsCodeOutput/vscodeData-" +
      today.toISOString().slice(0, 10) +
      today.getHours() +
      today.getMinutes() +
      today.getSeconds() +
      ".csv"
  );

  //create the csv file and write the header
  if (!fs.existsSync(outputPath)) {
    fs.writeFileSync(outputPath, "time,code\n");
  }

  //logs code every five seconds
  setInterval(() => {
    const editor = vscode.window.activeTextEditor;
    if (editor?.document) {
      const highlighted = editor!.document.getText();
      const now = new Date().getTime() / 1000;
      const data = `${now},"${highlighted}"\n`;

      ensureDirectoryExistence(outputPath);

      try {
        fs.appendFileSync(outputPath, data);
      } catch (err) {
        console.error(err);
      }
    }
  }, 5000);
}

function ensureDirectoryExistence(filePath: string) {
  /**
   * Checks if the filepath exists, if not it creates the necessary folders
   * @param {string} filePath - path to where you want to create a file
   */

  var dirname = path.dirname(filePath);
  if (fs.existsSync(dirname)) {
    return;
  }
  ensureDirectoryExistence(dirname);
  fs.mkdirSync(dirname);
}

export async function offerHelpNotification() {
  /**
   * Creates a notification to user offering to turn on copilot
   */

  let now = new Date().getTime();

  if (now - timeHelpPropmtWasActivated > 2 * 1000) {
    timeHelpPropmtWasActivated = now;

    const selection = await vscode.window.showWarningMessage(
      "Would you like help with your task?",
      "Yes, please",
      "No, thank you"
    );

    if (selection === "Yes, please") {
      activateCopilotChat();
    }
  }
}

export function activateCopilotChat() {
  vscode.commands.executeCommand("github.copilot.interactiveEditor.explain");
}

export function pauseNotification() {
  /**
   * FOR FUTURE WORK
   * Creates a notification to the user telling them they should take a break
   */

  let now = new Date().getTime();

  //only prompt if two minutes since last prompt
  if (now - timePausePropmtWasActivated > 2 * 60 * 1000) {
    timePausePropmtWasActivated = now;
    vscode.window.showWarningMessage(
      "You are approaching a level of stress that can be detrimental to your task. It might be time to take a break."
    );
  }
}

export function deactivate() {}
