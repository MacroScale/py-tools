console.log("index.js here and ready for you!")

var socket = io.connect('http://localhost:8080');

socket.on('connect', function() {
    console.log('Connected to server');
    // You can emit events here
    socket.emit('my_event', { data: 'Hello from client' });
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
});
