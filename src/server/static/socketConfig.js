console.log("socketsConfig.js here and ready for you!")

function createConnection(id){
    // Get the current host and port from the browser's location
    const host = window.location.hostname;  // This will get 'localhost' or the domain name

    // In production, if no port is specified, don't include it
    const port = window.location.port && window.location.port !== '80' && window.location.port !== '443'
        ? `:${window.location.port}`  // only append port if it's not 80 or 443
        : '';  // no port in production on default HTTP/HTTPS ports

    const protocol = window.location.protocol === 'https:' ? 'https' : 'http';
    const finalSocketUrl = `${protocol}://${host}${port}`;

    let socket = io.connect(finalSocketUrl, {
        query: {id: id}
    });

    socketLookup[id] = socket;

    socket.on('connect', function() {
        console.log(`Connected to server (Task ${id})`);
    });

    socket.on('disconnect', function() {
        console.log(`Disconnected from server (Task ${id})`);
    });

    socket.on('task_end', function(data) {
        console.log("task_end")
        console.log(data)
    });

    socket.on('stream', function(data) {
        const status = data.status
        const out = data.out

        const area = document.getElementById("terminal-"+id).getElementsByTagName("textarea")[0];
        const statusEl= document.getElementById("status-"+id);

        area.value = out
        statusEl.textContent = status;
    });
}

function removeSocket(id){
    socketLookup[id].close()
}

function killAllSocket(){
    for (id in socketLookup){
        socketLookup[id].close()
    }
}

var socketLookup = {}
