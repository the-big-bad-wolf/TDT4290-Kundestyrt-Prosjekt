import { activateCopilotChat, deactivate, offerHelpNotification, pauseNotification, setTimeHelpPropmtWasActivated  } from "../../extension";
import * as sinon from "sinon";
import * as vscode from "vscode";
import * as assert from "assert";

suite("Extension Test Suite", () => {
  let sandbox: sinon.SinonSandbox;

  setup(() => {
    sandbox = sinon.createSandbox();
  });

  teardown(() => {
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

    // Act
    await offerHelpNotification();
  
    // Assert
    assert.strictEqual(showWarningMessageStub.called, true, "Expected a warning message to be shown");
    assert.strictEqual(showWarningMessageStub.firstCall.args[0], "Would you like help with your task?");
    assert.deepStrictEqual(showWarningMessageStub.firstCall.args[1], yesOption.title);
    assert.deepStrictEqual(showWarningMessageStub.firstCall.args[2], noOption.title);
  });
});
