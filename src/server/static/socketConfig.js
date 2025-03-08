console.log("socketsConfig.js here and ready for you!")

function createConnection(id){
    let socket = io.connect('http://localhost:8080', {
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
        const out = data.stream_data.stdout
        const area = document.getElementById("terminal-"+id).getElementsByTagName("textarea")[0]
        area.value = out
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
