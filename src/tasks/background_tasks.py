import asyncio

from src.tasks.update_tool_scripts import update_tools_files

async def Start():
    async with asyncio.TaskGroup() as tg:
        tg = tg.create_task(update_tools_files())
