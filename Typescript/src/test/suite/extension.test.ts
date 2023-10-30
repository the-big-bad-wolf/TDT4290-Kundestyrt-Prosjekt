import { deactivate, pauseNotification } from "../../extension";
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
    const showWarningMessageStub = sandbox.stub(vscode.window, "showWarningMessage");
    const twoMinutesAgo = new Date().getTime() - (2 * 60 * 1000 + 1);
    pauseNotification(twoMinutesAgo);
    assert.strictEqual(showWarningMessageStub.called, true);
  });

  test("pauseNotification should not show a warning message if the last prompt was less than 2 minutes ago", () => {
    const showWarningMessageStub = sandbox.stub(vscode.window, "showWarningMessage");
    const oneMinuteAgo = new Date().getTime() - (1 * 60 * 1000);
    pauseNotification(oneMinuteAgo);
    assert.strictEqual(showWarningMessageStub.called, false);
  });
});
