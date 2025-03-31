export function connectToChat(teamId, onMessageReceived) {
    const socket = new WebSocket(`ws://localhost:8000/ws/chat/${teamId}`);

    socket.onopen = () => {
        console.log("Connected to chat");
    };

    socket.onmessage = (event) => {
        onMessageReceived(event.data);
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    return socket;
}
