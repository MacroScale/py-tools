import asyncio
from src.server import server
from src.tasks import background_tasks
from src.task_manager import task_manager 

async def main():
    try: 
        await asyncio.gather(
            server.Start(),
            background_tasks.Start()
        )
    except:
        print("program exited")

if __name__ == "__main__":
    asyncio.run(main())
