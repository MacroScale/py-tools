import asyncio

from src.tasks.update_tool_scripts import update_tools_files
from src.tasks.dispatch_out_tools import dispatch_out_tools
from src.tasks.dispatch_task_end import dispatch_task_end

async def Start():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(update_tools_files())
        task2 = tg.create_task(dispatch_out_tools())
        task3 = tg.create_task(dispatch_task_end())
