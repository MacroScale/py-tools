from subprocess import Popen, PIPE, CalledProcessError
import threading
import sys
import time 
import io 
import os 
import select 
import fcntl

from src.task_manager.slog import Slog 

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self._lock = threading.Lock()

    def stream_output(self, task_id):
        process = self.tasks[task_id]["process"]

        # set stdout and stderr to non-blocking mode
        for stream in [process.stdout, process.stderr]:
            fd = stream.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        while process.poll() is None:
            readable, _, _ = select.select([process.stdout, process.stderr], [], [])

            for stream in readable:
                data = stream.read()
                if not data: continue;

                if stream == process.stdout:
                    with self._lock:
                        self.tasks[task_id]["slogger"].add_log("out", data)
                else:
                    with self._lock:
                        self.tasks[task_id]["slogger"].add_log("err", data)

        with self._lock:
            self.tasks[task_id]["status"] = "not_running"

            script_arr = self.tasks[task_id]["tool_path"].split("/")
            script_name = script_arr[len(script_arr)-1]
            self.tasks[task_id]["slogger"].add_log("os", f"task ended: {script_name}\n")

    def run_script(self, tool_path, task_id):
        try:
            process = Popen([sys.executable, "-u", tool_path],
                                       stdout=PIPE,
                                       stderr=PIPE,
                                       bufsize=1,
                                       universal_newlines=True,
                                       text=True,
                                )
            with self._lock:
                self.tasks[task_id]["process"] = process
                self.tasks[task_id]["status"] = "running"

            thread = threading.Thread(target=self.stream_output, args=(task_id,))
            self.tasks[task_id]["stream_output_thread"] = thread 
            self.tasks[task_id]["stream_output_thread"].start()

        except FileNotFoundError:
            with self._lock:
                self.tasks[task_id]["status"] = "error"
                self.tasks[task_id]["stderr"] = f"Error: Script '{tool_path}' not found."
                self.tasks[task_id]["returncode"] = -1
        except Exception as e:
            with self._lock:
                self.tasks[task_id]["status"] = "error"
                self.tasks[task_id]["stderr"] = f"An error occurred: {str(e)}"
                self.tasks[task_id]["returncode"] = -1

    def start_task(self, tool_path: str, tool_id: int):
        if tool_id not in self.tasks:
            self.tasks[tool_id] = {
                     "tool_id": tool_id, 
                     "tool_path": tool_path, 
                     "status": "waiting",
                     "process": None,
                     "thread": None,
                     "returncode": None,
                     "stream_thread": None,
                     "slogger": Slog(),
                     "stdout": "",
                     "stderr": "" 
                }

        thread = threading.Thread(target=self.run_script, args=(tool_path, tool_id))
        self.tasks[tool_id]["thread"] = thread
        thread.start()
        print("\ntask start:", tool_path, "\n")
        self.init_task_log(tool_id)

    def init_task_log(self, task_id):
        with self._lock:
            if task_id in self.tasks:
                script_arr = self.tasks[task_id]["tool_path"].split("/")
                script_name = script_arr[len(script_arr)-1]
                self.tasks[task_id]["slogger"].add_log("os", f"task started: {script_name}\n")

    def get_task_info(self, task_id):
        with self._lock:
            if task_id in self.tasks:
                return dict(self.tasks[task_id])
        return None

    def is_running(self, task_id):
        with self._lock:
            if task_id in self.tasks:
                return self.tasks[task_id]["status"] == "running"
        return None

    def exists(self, task_id):
        with self._lock:
            if task_id in self.tasks:
                return True
        return False 

    def get_output(self, task_id: int):
        with self._lock:
            if task_id in self.tasks:
                return self.tasks[task_id]["slogger"].get_logs()
        return "";

    def get_status(self, task_id: int):
        with self._lock:
            if task_id in self.tasks:
                return self.tasks[task_id]["status"]
        return "not_running"

    def delete_task(self, task_id: int):
        task_info = self.get_task_info(task_id)
        if not task_info: return
        if task_info["process"] and task_info["process"].poll() is not None:
            with self._lock:
                del self.tasks[task_id]

    def stop_all_tasks(self):
        for task_id in self.tasks:
            task_info = self.tasks[task_id]
            if task_info and task_info["process"]:
                task_info["process"].terminate()

    def stop_task(self, task_id):
        task_info = self.get_task_info(task_id)
        if task_info and task_info["process"] and task_info["stream_output_thread"]:
            task_info["process"].terminate()
            task_info["status"] = "not_running"

            script_arr = self.tasks[task_id]["tool_path"].split("/")
            script_name = script_arr[len(script_arr)-1]
            self.tasks[task_id]["slogger"].add_log("os", f"task forcefully ended: {script_name}\n")

            print(f"Task {task_id} terminated.")

task_manager = TaskManager()
