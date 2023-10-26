import { Server as MockServer } from "mock-socket";
import { setUp } from "../../listener";

test("WebSocket message handling", (done) => {
  const mockServer = new MockServer("ws://localhost:8080");

  mockServer.on("connection", (socket: any) => {
    socket.send("Your mock message here");
  });

  setUp(true);

  // Assertions related to the expected behavior upon receiving the mock message
  // ...

  mockServer.stop(done);
});
