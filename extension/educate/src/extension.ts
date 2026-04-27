// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('educate.educate', async () => {

		const editor = vscode.window.activeTextEditor;

		if(!editor) return;


		const selection = editor?.selection;
		const selectedText = editor?.document.getText(selection);
		const startLine = editor?.selection.start.line

		const response = await fetch("https://educate-backend-539946496244.australia-southeast1.run.app/educate", {
			method: "POST",
			headers: {	"Content-Type": "application/json"},
			body: JSON.stringify({code_snippet: selectedText})
		});
		const data = await response.json();

		editor.edit(editBuilder => {
			editBuilder.insert(new vscode.Position(startLine, 0), buildComments(data));
		})

		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Help generated from educate!');
	});

	context.subscriptions.push(disposable);
}

function buildComments(data:{ docs: string[], summary: string, improvements: string[]}) : string {
	const docs: string[] = [];
	let summary: string = "";
	const improvements: string[] = [];
	for (const doc of data.docs) {
		const line = "# " + doc;
		docs.push(line);
	}
	summary = "# " + data.summary;
	for (const improv of data.improvements) {
		const line = '# ' + improv;
		improvements.push(line);
	};

	const allLines = [...docs, summary, ...improvements];
	return allLines.join("\n") + "\n";
	
};

// This method is called when your extension is deactivated
export function deactivate() {}
