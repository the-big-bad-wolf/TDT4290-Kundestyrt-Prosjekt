# TDT4290-Kundestyrt-Prosjekt

Repository for TDT4290 Customer Driven Project - Group 4 - 2023

## Team members

| Name                          |
| ----------------------------- |
| Bjørn Eirik Melaaen           |
| Elisabeth Krogstad Iversen    |
| Haakon Liu Selnes             |
| Mikkel Andreas Ask Guttormsen |
| Synne Frafjord Moe            |

## Supervisor

| Name              |
| ----------------- |
| Isabella Possaghi |

## Customer

| Name           |
| -------------- |
| Kshitij Sharma |

## How to run
Before you start you need to have Python and Node.js installed on your machine.

You need to start the Python backend before you activate the VSCode extension. To start the eyetracker and start calculating and forecasting your cognitive load, simply run "main.py" in the "Python" folder. First time you run the program you will have to install the dependencies with the following command:
```
pip install -r requirements.txt
```

To use the VSCode extension you can either open the project in VSCode and run it, or you can install the extension with the provided "extension-0.0.1.vsix" file.

1. To run the extension directly from the project files, you first need to open the "Typescript" folder as root in VSCode so that VSCode will detect the config files and automatically compile the extension when you run it. Then you have to install the project dependencies with the command `npm install`. Then open /src/extension.ts. Then you can run the command "Start Debugging" or "Run Without Debugging" by either pressing f5 or ctrl+f5 respectively, or by clicking "Run" in VSCode and selecting the command. This will open a new window where the extension is installed.

2. To install the extension with the provided "extension-0.0.1.vsix" file, go to the extension view, and click on the three dots in the right upper corner. Chose to install as vsix, and locate the vsix file on your computer. Alternatively, in the terminal, run the following command:
```
code--install-extension path\extension-0.0.1.vsix
```

After the extension is installed, open the command palette by pressing ctrl+shift+p in windows or cmd+shift+p on mac, and type "AI Initiated Help" if you want the system to prompt the user when cognitive load is too high or low, or "User Initiated Help" if you want a help button that the user can click themselves to get help. This will activate the extension and display a notification that the extension is calculating a baseline. When the baseline has been calculated, your cognitive load or a help button should be displayed in the status bar, depending on whether you selected AI or user initiated help. If you have selected "AI Initiated Help" and your observed or forecasted cognitive load is two standard deviations or more from the baseline mean, you should get a pop-up in VSCode asking whether you want help, and if you click yes GitHub Copilot should automatically explain the file you are currently located in. If you have selected "User Initiated Help" the "Help me!" button should get GitHub Copilot to explain the file you are located in like for the AI initiated help.


## How to run tests

### Python tests

In the terminal, in the python folder, run the command `python -m pytest`

### Typescript tests

In the terminal, in the typescript folder, run the command `npm run test`.
