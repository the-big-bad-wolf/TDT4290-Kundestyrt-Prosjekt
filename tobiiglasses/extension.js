const vscode = require('vscode');

let statusBarItem;
let counter = 0;
let secondCounter = 0;

function activate(context) {
    // Opprett statusbaren
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = `Counter: ${counter}, secondCounter: ${secondCounter}`;
    statusBarItem.show();

    // Sett opp en intervallfunksjon for å øke telleren og oppdatere statusbaren hver sekund
    setInterval(() => {
        counter++;
        secondCounter += 2;
        //vi må sette statusteksten i hvert intervall for å vise oppdatert informasjon
        statusBarItem.text = `Counter: ${counter}, SecondCounter: ${secondCounter}`;
    }, 1000);

    context.subscriptions.push(statusBarItem); // Husk å legge den til i subscriptions for opprydding
}

exports.activate = activate;
