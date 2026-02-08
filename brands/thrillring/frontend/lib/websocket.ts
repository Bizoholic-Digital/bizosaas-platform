export class WebSocketClient {
    connect(url: string) {
        console.warn("WebSocketClient stub called");
    }

    disconnect() {
        console.warn("WebSocketClient disconnect stub");
    }

    on(event: string, callback: Function) {
        // Stub event listener
    }
}

export const websocketClient = new WebSocketClient();

export const useWebSocket = () => ({
    status: 'connected',
    messages: [],
    send: (msg: any) => { }
});

export default websocketClient;
