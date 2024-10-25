## How to run
Before you start you need to have Python 3.10 and Node.js installed on your machine. You also need to have installed the "Github Copilot" and "Github Copilot Chat" VSCode extensions and an active Copilot license on your Github account. You also need have connected an eye-tracker capable of detecting pupil diameters that is also compatible with the Tobii Pro SDK. A list of compatible devices can be found here: https://developer.tobiipro.com/tobiiprosdk/supportedeyetrackers.html. For instructions regarding driver installation for your Tobii eye-tracker, see documentation for your device at https://connect.tobii.com/.

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

## Parameters

In the backend there is a setup.cfg file where you can change parameters such as how far into the future to forecast, how many observations used to create a baseline and how many historical observations used to create forecasting model.
