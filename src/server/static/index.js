document.addEventListener('DOMContentLoaded', function(){
    const startBtns = Array.from(document.getElementsByClassName("start-task"));
    const endBtns = Array.from(document.getElementsByClassName("end-task"));

    startBtns.forEach(el => el.addEventListener("click", startTask))
    endBtns.forEach(el=> el.addEventListener("click", endTask))
});

var timePreviousAction = Date.now();
var timeoutPeriod = 2 * 1000;

async function startTask(event){
    if (timePreviousAction+timeoutPeriod > Date.now()) { return; }
    timePreviousAction = Date.now() 

    id = Number(event.target.getAttribute("data-id").split("-")[1])

    try {
        if (scriptsStatusLookup[id].status == "not_running"){
            console.log("starting task:", id)
            // send request to start task and wait for 200 resp
            let resp = await fetch(`/api/start/${id}`);
            let respData = await resp.json()
            console.log(respData)
            if (resp.status !== 200) {throw Error("server failed to respond with 200")}

            // once task has started then create a socket connection
            createConnection(id)
            updateStatus(id, "running")
        }
    }
    catch (err){
        console.log("Error starting task:", err)
        return;
    }
}

async function endTask(event){
    if (timePreviousAction+timeoutPeriod > Date.now()) { return; }
    timePreviousAction = Date.now() 


}

function updateStatus(id, status){
    const buttons = Array.from(document.getElementsByClassName("cur-status"));
    const el = buttons.filter(x => x.getAttribute("data-id").split("-")[1] == id.toString())[0]
    el.innerText = status

    scriptsStatusLookup[id].status = status
}
