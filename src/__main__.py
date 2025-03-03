import asyncio
from src.server import server
from src.tasks import background_tasks
from src.task_manager import task_manager 

async def main():
    # Run both tasks concurrently
    await asyncio.gather(
        server.Start(),
        background_tasks.Start()
    )

if __name__ == "__main__":
    asyncio.run(main())
