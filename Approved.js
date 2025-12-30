const socket = new WebSocket('ws://localhost:8000/ws/pulse');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    document.getElementById('digestive-track').innerText = JSON.stringify(data, null, 2);

    if (data.stability_score > 0.8) {
        document.getElementById('launchpad').innerText = "Insight ready: " + JSON.stringify(data);
    }
};

function sendSignal(text) {
    socket.send(text);
}
