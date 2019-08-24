from flask_script import Command, Option


class GunicornServer(Command):

    description = 'Run the app within Gunicorn'

    def __init__(self, host='0.0.0.0', port=8080, workers=16, timeout=30, max_requests=20, loglevel="debug"):
        self.port = port
        self.host = host
        self.workers = workers
        self.timeout = timeout
        self.max_requests = max_requests
        self.loglevel = loglevel

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),

            Option('-t', '--timeout',
                   dest='timeout',
                   type=int,
                   default=self.timeout),
            Option('--max-requests',
                   dest='max_requests',
                   type=int,
                   default=self.max_requests),
            Option('--log-level',
                   dest='loglevel',
                   type=str,
                   default=self.loglevel)
        )

    def __call__(self, app, host, port, workers, timeout, max_requests, loglevel):

        from gunicorn import version_info

        if version_info < (0, 9, 0):
            from gunicorn.arbiter import Arbiter
            from gunicorn.config import Config
            arbiter = Arbiter(
                Config({'bind': "%s:%d" % (host, int(port)), 'workers': workers}),
                app
            )
            arbiter.run()
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers,
                        'timeout': timeout,
                        'max_requests': max_requests,
                        'loglevel': loglevel
                    }

                def load(self):
                    return app

            FlaskApplication().run()
