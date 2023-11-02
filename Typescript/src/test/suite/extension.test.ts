import {
  activateCopilotChat,
  deactivate,
  initializeHelpButton,
  offerHelpNotification,
  pauseNotification,
  setUpStatusbar,
  setTimeHelpPropmtWasActivated,
  getStatusBarItem,
  updateStatusBarData,
  log,
  setPauseNotification,
} from "../../extension";
import * as sinon from "sinon";
import * as vscode from "vscode";
import * as assert from "assert";
import * as fs from "fs";

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

  /**
   * Test case for the `deactivate` function to verify that it does nothing and doesn't throw an error.
   */
  test("deactivate should do nothing", () => {
    assert.doesNotThrow(() => deactivate());
  });

  /**
   * Test case for `pauseNotification` function when the last prompt was more than 2 minutes ago.
   */
  test("pauseNotification should show a warning message if the last prompt was more than 2 minutes ago", () => {
    // Arrange
    setPauseNotification(new Date().getTime() - (2 * 60 * 1000 + 1)); // set to more than 2 minutes ago
    const showWarningMessageStub = sandbox.stub(
      vscode.window,
      "showWarningMessage"
    );

    // Act
    pauseNotification();

    // Assert
    assert.strictEqual(
      showWarningMessageStub.called,
      true,
      "Expected a warning message to be shown"
    );
  });

  /**
   * Test case for `pauseNotification` function when the last prompt was less than 2 minutes ago.
   */
  test("pauseNotification should not show a warning message if the last prompt was less than 2 minutes ago", () => {
    // Arrange
    setPauseNotification(new Date().getTime() - (2 * 60 * 1000 - 1)); // set to less than 2 minutes ago
    const showWarningMessageStub = sandbox.stub(
      vscode.window,
      "showWarningMessage"
    );

    // Act
    pauseNotification();

    // Assert
    assert.strictEqual(
      showWarningMessageStub.called,
      false,
      "Expected no warning message to be shown"
    );
  });

  /**
   * Test case for `activateCopilotChat` function to ensure it executes the correct command.
   */
  test("activateCopilotChat should execute the correct command", () => {
    // Arrange
    const executeCommandStub = sandbox.stub(vscode.commands, "executeCommand");

    // Act
    activateCopilotChat();

    // Assert
    assert.strictEqual(
      executeCommandStub.calledWith("github.copilot.interactiveEditor.explain"),
      true,
      "Expected Copilot command to be executed"
    );
  });

  /**
   * Test case for `offerHelpNotification` function to show a warning message with options.
   */
  test("offerHelpNotification should show a warning message with the correct options", async () => {
    // Arrange
    const yesOption: vscode.MessageItem = { title: "Yes, please" };
    const noOption: vscode.MessageItem = { title: "No, thank you" };
    const showWarningMessageStub = sandbox
      .stub(vscode.window, "showWarningMessage")
      .resolves(yesOption);

    // Act
    // Set timeHelpPropmtWasActivated to more than 2 minutes ago
    setTimeHelpPropmtWasActivated(new Date().getTime() - (2 * 60 * 1000 + 1));
    await offerHelpNotification();

    // Assert
    assert.strictEqual(
      showWarningMessageStub.called,
      true,
      "Expected a warning message to be shown"
    );
    assert.strictEqual(
      showWarningMessageStub.firstCall.args[0],
      "Would you like help with your task?"
    );
    assert.deepStrictEqual(
      showWarningMessageStub.firstCall.args[1],
      yesOption.title
    );
    assert.deepStrictEqual(
      showWarningMessageStub.firstCall.args[2],
      noOption.title
    );
  });

  /**
   * Test case for `initializeHelpButton` function to create and display a button.
   */
  test("initializeHelpButton should create and display button", () => {
    // Arrange. Initialize statusbar
    setUpStatusbar();

    // Act
    initializeHelpButton();

    // Assert
    assert.strictEqual(
      getStatusBarItem().text,
      `Help me!`,
      "Expected button text to be 'Help me!'"
    );
    assert.strictEqual(
      typeof getStatusBarItem().command,
      "string",
      "Expected button command to be a string"
    );
  });

  test("updateStatusBarData should update status bar text with cognitive load", () => {
    //Arrange
    // Define your data as a JavaScript object
    const data = {
      "Current cognitive load": "low",
    };
    // Convert the JavaScript object to a JSON string
    const jsonData = JSON.stringify(data);
    // Create a Buffer from the JSON string
    const bufferData = Buffer.from(jsonData);

    //Act
    // Now you can use the bufferData variable
    updateStatusBarData(bufferData);

    // Assert
    assert.strictEqual(
      getStatusBarItem().text,
      "cognitive load: low",
      "Expected status bar text to be 'low'"
    );
  });

  /**
   * Test case for `log` function to append data to a file.
   */
  test("log should append data to file", () => {
    // Arrange
    const outputPath = "path/to/file";
    const data = "some data";
    const appendFileSyncStub = sandbox.stub(fs, "appendFileSync");

    // Act
    log(outputPath, data);

    // Assert
    assert.strictEqual(
      appendFileSyncStub.calledWith(outputPath, data),
      true,
      "Expected data to be appended to file"
    );
  });
});
