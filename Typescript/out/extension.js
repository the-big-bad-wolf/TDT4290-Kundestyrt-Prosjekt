"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const listener_1 = require("./listener");
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "extension" is now active!');
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand("extension.showData", async () => {
        // The code you place here will be executed every time your command is executed
        // Display a message box to the user
        const message = await (0, listener_1.fetchData)();
        if (message) {
            vscode.window.showInformationMessage(message);
        }
        else {
            vscode.window.showErrorMessage("Failed to fetch data from Server.py.");
        }
        vscode.window.showInformationMessage("Now logging changes in open file");
    });
    //When the text in the document is changed
    //console.log() the whole document
    vscode.workspace.onDidChangeTextDocument(event => {
        console.log(event.document.getText());
    }, null, context.subscriptions);
    context.subscriptions.push(disposable);
}
exports.activate = activate;
// This method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map