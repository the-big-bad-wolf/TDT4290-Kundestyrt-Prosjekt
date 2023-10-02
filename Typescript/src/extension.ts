// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import { setUp } from "./listener";
import * as fs from "fs";
import * as path from "path";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log('Congratulations, your extension "extension" is now active!');

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  const disposable = vscode.commands.registerCommand(
    "extension.showData",
    () => {
      // The code you place here will be executed every time your command is executed
      // Display a message box to the user
      setUp();
      vscode.window.showInformationMessage("tjohei");
    },
    context.subscriptions
  );

  let today = new Date();

  //checks if the output folder already exists,
  //if not it creates it
  function ensureDirectoryExistence(filePath: string) {
    var dirname = path.dirname(filePath);
    if (fs.existsSync(dirname)) {
      return true;
    }
    ensureDirectoryExistence(dirname);
    fs.mkdirSync(dirname);
  }

  let outputPath = path.join(
    __dirname,
    "../../vsCodeOutput/vscodeData-" +
      today.toISOString().slice(0, 10) +
      today.getHours() +
      today.getMinutes() +
      ".csv"
  );
  //logs the code in open file to csv file every five seconds
  //along with the time
  setInterval(() => {
    const editor = vscode.window.activeTextEditor;
    const highlighted = editor!.document.getText();
    const now = new Date().toLocaleString();

    const data = `${now},\n${highlighted}\n`;

    ensureDirectoryExistence(outputPath);

    try {
      fs.appendFileSync(outputPath, data + "\n\n");
    } catch (err) {
      console.error(err);
    }
  }, 5000);

  context.subscriptions.push(disposable);
}

export async function offerHelpNotification() {
  /**
   * Creates a notification to user offering to turn on copilot
   */

  const selection = await vscode.window.showWarningMessage(
    "Do you want some help with that?",
    "Yes, please",
    "No, thank you"
  );

  if (selection == "Yes, please") {
    console.log("Turn on copilot");
  } else if (selection == "No, thank you") {
    console.log("The user does not need help");
  }
}

export function pauseNotification() {
  /**
   * Creates a notification to the user telling them they should take a break
   */

  vscode.window.showWarningMessage(
    "Hey there, you seem stressed. Maybe its time to take a break?"
  );
}

// This method is called when your extension is deactivated
export function deactivate() {}
