// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import { setUp } from "./listener";
import * as fs from "fs";
import * as path from "path";

// This method is called when your extension is activated
export function activate(context: vscode.ExtensionContext) {
  console.log('Congratulations, your extension "extension" is now active!');

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

  //logs code every five seconds
  setInterval(() => {
    const editor = vscode.window.activeTextEditor;
    const highlighted = editor!.document.getText();
    const now = new Date().toLocaleString();
    const data = `${now},\n${highlighted}\n`;

    log(data);
  }, 5000);

  context.subscriptions.push(disposable);
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

// This method is called when your extension is deactivated
export function deactivate() {}
