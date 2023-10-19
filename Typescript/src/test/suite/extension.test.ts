import * as assert from 'assert';

// You can import and use all API from the 'vscode' module
// as well as import your extension to test it
import * as vscode from 'vscode';
import { activateCopilotChat, offerHelpNotification, pauseNotification } from '../../extension';
// import * as myExtension from '../../extension';

suite('Extension Test', () => {

	suiteSetup(done => {
        // setup logic if needed
        done();
    });

    suiteTeardown(done => {
        // cleanup logic if needed
        done();
    });
	
	test('Sample test', () => {
		assert.strictEqual(-1, [1, 2, 3].indexOf(5));
		assert.strictEqual(-1, [1, 2, 3].indexOf(0));
	});

	test('Offer Help Notification', async () => {
        // This test checks if the help notification function works, though in a test environment, UI functionalities might not be visible
        await offerHelpNotification();
        // TODO: Additional assertions can be added here to verify behavior
    });

	test('Pause Notification', async () => {
        // Test for pause notification
        await pauseNotification();
        // TODO: Like the help notification, you might need to check if the function runs without errors
    });

	test('Activate Copilot Chat', () => {
        // Test if copilot chat activation works
        activateCopilotChat();
        // TODO: In a test environment, you might not be able to verify this behavior. This just checks if the function runs without errors
    });
});
