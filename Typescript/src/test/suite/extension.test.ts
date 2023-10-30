import { activateCopilotChat, deactivate, initializeHelpButton, offerHelpNotification, pauseNotification, setUpStatusbar, setTimeHelpPropmtWasActivated, getStatusBarItem, updateStatusBarData, log, ensureDirectoryExistence  } from "../../extension";
import * as sinon from "sinon";
import * as vscode from "vscode";
import * as assert from "assert";
import * as fs from "fs";
import { RawData } from "ws";

/**
 * Extension Test Suite.
 */
suite("Extension Test Suite", () => {
  let sandbox: sinon.SinonSandbox;

  /**
   * Sets up the test environment before each test case.
   * @function
   */
  setup(() => {
    // Create a Sinon sandbox to isolate function behavior.
    sandbox = sinon.createSandbox();
  });

  /**
   * Tears down the test environment after each test case.
   * @function
   */
  teardown(() => {
    // Restore the Sinon sandbox to its original state.
    sandbox.restore();
  });

  test("deactivate should do nothing", () => {
    assert.doesNotThrow(() => deactivate());
  });

  
  test("pauseNotification should show a warning message if the last prompt was more than 2 minutes ago", () => {
    // Arrange
    const showWarningMessageStub = sandbox.stub(vscode.window, "showWarningMessage");
    const twoMinutesAgo = new Date().getTime() - (2 * 60 * 1000 + 1);

    // Act
    pauseNotification(twoMinutesAgo);

    // Assert
    assert.strictEqual(showWarningMessageStub.called, true, "Expected a warning message to be shown");
  });

  test("pauseNotification should not show a warning message if the last prompt was less than 2 minutes ago", () => {
    // Arrange
    const showWarningMessageStub = sandbox.stub(vscode.window, "showWarningMessage");
    const oneMinuteAgo = new Date().getTime() - (1 * 60 * 1000);

    // Act
    pauseNotification(oneMinuteAgo);

    // Assert
    assert.strictEqual(showWarningMessageStub.called, false, "Expected no warning message to be shown");
  });

  test("activateCopilotChat should execute the correct command", () => {
    // Arrange
    const executeCommandStub = sandbox.stub(vscode.commands, "executeCommand");
  
    // Act
    activateCopilotChat();
  
    // Assert
    assert.strictEqual(executeCommandStub.calledWith("github.copilot.interactiveEditor.explain"), true, "Expected Copilot command to be executed");
  });
  
  test("offerHelpNotification should show a warning message with the correct options", async () => {
    const yesOption: vscode.MessageItem = { title: "Yes, please" };
    const noOption: vscode.MessageItem = { title: "No, thank you" };
    const showWarningMessageStub = sandbox.stub(vscode.window, "showWarningMessage").resolves(yesOption);
  
    // Set timeHelpPropmtWasActivated to more than 2 minutes ago
    setTimeHelpPropmtWasActivated(new Date().getTime() - (2 * 60 * 1000 + 1));

    
    await offerHelpNotification();
  
    // Assert
    assert.strictEqual(showWarningMessageStub.called, true, "Expected a warning message to be shown");
    assert.strictEqual(showWarningMessageStub.firstCall.args[0], "Would you like help with your task?");
    assert.deepStrictEqual(showWarningMessageStub.firstCall.args[1], yesOption.title);
    assert.deepStrictEqual(showWarningMessageStub.firstCall.args[2], noOption.title);
  });

  test("initializeHelpButton should create and display button", () => {
    // Initialize statusbar
    setUpStatusbar();
    
    // Act
    initializeHelpButton();

    // Assert
    assert.strictEqual(getStatusBarItem().text, `Help me!`, "Expected button text to be 'Help me!'");
    assert.strictEqual(typeof getStatusBarItem().command, "string", "Expected button command to be a string");
  });

  test("updateStatusBarData should update status bar text with cognitive load", () => {
    // Define your data as a JavaScript object
    const data = {
      "Current cognitive load": "low"
    };

    // Convert the JavaScript object to a JSON string
    const jsonData = JSON.stringify(data);

    // Create a Buffer from the JSON string
    const bufferData = Buffer.from(jsonData);

    // Now you can use the bufferData variable
    updateStatusBarData(bufferData);

    // Assert
    assert.strictEqual(getStatusBarItem().text, "cognitive load: low", "Expected status bar text to be 'low'");
  });

  test("log should append data to file", () => {
    // Arrange
    const outputPath = "path/to/file";
    const data = "some data";
    const appendFileSyncStub = sandbox.stub(fs, "appendFileSync");

    // Act
    log(outputPath, data);

    // Assert
    assert.strictEqual(appendFileSyncStub.calledWith(outputPath, data), true, "Expected data to be appended to file");
  });
});
