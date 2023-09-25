import * as WebSocket from "ws";

export function setUp() {
	console.log("heu");
	const wss = new WebSocket.Server({ port: 8080 });

	wss.on("connection", ws => {
		console.log("New client connected");
	});

	wss.on("message", (message: any) => {
		console.log(`Received message => ${message}`);
	});

	console.log("Server started at http://127.0.0.1:8080");
}
