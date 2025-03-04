console.log("socketsConfig.js here and ready for you!")

function initScriptsDict(){
    const buttons = Array.from(document.getElementsByClassName("accordion-item"));
    const id_status = buttons.map(el => {
        return {
            "id": Number(el.getAttribute("data-id").split("-")[1]),
            "status": el.getAttribute("data-status")
        }
    })
    return id_status
}

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

    socket.on('stream', function(data) {
        const out = data.stream_data.stdout
        const area = document.getElementById("terminal-"+id).getElementsByTagName("textarea")[0]
        area.value = out
    });
}

function initSockets(){
    runningTasks = scriptsStatusLookup.filter(el => el.status == "running") 

    for (task in runningTasks){
        createConnection(task.id)
    }
}

function killAllSocket(){
    for (id in socketLookup){
        socketLookup[id].close()
    }
}

var socketLookup = {}
var scriptsStatusLookup = initScriptsDict()

initSockets()
