from gevent import monkey
monkey.patch_all()
import gevent 

from src.server import server, app_server 
from src.tasks import background_tasks

def main():
    try:
        server_glet = gevent.spawn(server.Start)
        background_glet = gevent.spawn(background_tasks.Start)

        background_glet.join()
        server_glet.join()

    except Exception as e:
        print(f"Program exited with error: {e}")

if __name__ == "__main__":
    main()
    
application = app_server # for gunicorn
