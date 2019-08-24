from flask_script import Manager, Server
from custom_api.server import create_app
from custom_api.custom_wsgi import GunicornServer
from custom_api.models.seed import seed as seed_procedure



manager = Manager(create_app())

# I've left the config option due to manager.run() doesn't recognize config values like host and port
# manager.add_option('-c', '--config', dest='config', required=False)
server = Server(host=manager.app.config['HOST'],
                port=manager.app.config['PORT'])
manager.add_command("runserver", GunicornServer(host=manager.app.config['HOST'],
                                                port=manager.app.config['PORT'],
                                                workers=manager.app.config['WORKERS'],
                                                timeout=manager.app.config['TIMEOUT'],
                                                max_requests=manager.app.config['MAX_REQUESTS']
                                                ))
manager.add_command("run-debug-mode", server)


@manager.command
def seed():
    seed_procedure()

if __name__ == "__main__":
    manager.run()
