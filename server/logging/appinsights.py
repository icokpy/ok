from applicationinsights.logging import LoggingHandler
from applicationinsights.requests import WSGIApplication


class AppInsights(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.key = app.config.get("APPLICATION_INSIGHTS_KEY")
        if not self.key:
            return

        self.middleware = WSGIApplication(self.key, app.wsgi_app)
        app.wsgi_app = self.middleware

        self.log_handler = LoggingHandler(self.key)
        app.logger.addHandler(self.log_handler)
