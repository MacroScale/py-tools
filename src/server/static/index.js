document.addEventListener('DOMContentLoaded', async function(){
    const startBtns = Array.from(document.getElementsByClassName("start-task"));
    const endBtns = Array.from(document.getElementsByClassName("end-task"));

    startBtns.forEach(el => el.addEventListener("click", startTask))
    endBtns.forEach(el=> el.addEventListener("click", endTask))

    await init()
});

var timePreviousAction = Date.now();
var timeoutPeriod = 2 * 1000;

async function startTask(event){
    if (timePreviousAction+timeoutPeriod > Date.now()) { return; }
    timePreviousAction = Date.now() 

    id = Number(event.target.getAttribute("data-id").split("-")[1])

    try {
        //if (scriptsStatusLookup.filter(x => x.id==id)[0].status == "not_running"){
            console.log("starting task:", id)
            // send request to start task and wait for 200 resp
            let resp = await fetch(`/api/start/${id}`);
            let respData = await resp.json()

            console.log(respData)
            if (respData.status !== 200) {
                throw Error(`server error (${respData.status}): ${respData.err}`)
            }

            // once task has started then create a socket connection
            createConnection(id)
            let taskList = await getTaskList()
            updateStatus(taskList)
        //}
    }
    catch (err){
        console.log("Error starting task:", err)
        return;
    }
}

async function endTask(event){
    if (timePreviousAction+timeoutPeriod > Date.now()) { return; }
    timePreviousAction = Date.now() 

    id = Number(event.target.getAttribute("data-id").split("-")[1])

    try {
        //if (scriptsStatusLookup.filter(x => x.id==id)[0].status == "not_running"){
            console.log("ending task:", id)
            // send request to start task and wait for 200 resp
            let resp = await fetch(`/api/end/${id}`);
            let respData = await resp.json()

            console.log(respData)
            if (respData.status !== 200) {
                throw Error(`server error (${respData.status}): ${respData.err}`)
            }

            let taskList = await getTaskList()
            updateStatus(taskList)
        //}
    }
    catch (err){
        console.log("Error starting task:", err)
        return;
    }
}

function updateStatus(taskList){
    let els = document.getElementsByClassName("cur-status");

    for (let i=0; i<els.length; ++i) {
        let el = els[i];
        let id = Number(el.getAttribute("data-id").split("-")[1]);

        let filteredTasks = taskList?.task_list?.filter((task) => task.tool_id == id) || [];
        let newStatus = filteredTasks.length > 0 ? filteredTasks[0].status : "not_running";

        el.textContent = newStatus;
    } 
}

async function getTaskList(){
    let resp = await fetch("/api/tasklist");
    let respData = await resp.json()
    return respData
}

async function initSockets(taskList){
    try{
        for (idx in taskList.task_list){
            let el = taskList.task_list[idx]
            createConnection(el.tool_id)
        }
    } catch(err){
        console.log("ERROR initSockets:", err);
    }
}

async function init(){
    taskList = await getTaskList()
    initSockets(taskList)
    updateStatus(taskList)
}
