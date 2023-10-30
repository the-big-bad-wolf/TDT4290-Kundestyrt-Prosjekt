import * as sinon from "sinon";
import { setUp } from "../../listener";
import * as WebSocket from "ws";
import * as assert from "assert";

suite("Listener Test Suite", () => {
  let sandbox: sinon.SinonSandbox;
  let server: WebSocket.Server;
  let client: WebSocket;

  setup(() => {
    sandbox = sinon.createSandbox();
  });

  teardown(() => {
    sandbox.restore();
    server.close();
    client.close();
  });

  test("WebSocket should connect to server", (done) => {
    server = new WebSocket.Server({ port: 0 }, () => {
      const port = (server.address() as WebSocket.AddressInfo).port;
      client = new WebSocket(`ws://localhost:${port}`);
      client.on("open", () => {
        done();
      });
      setUp(false);
    });
  });
});
