class LoggerMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Log incoming path
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')
        print(f"[WSGI Middleware] Request: {method} {path}")

        # Wrap the start_response to capture status
        def custom_start_response(status, headers, exc_info=None):
            print(f"[WSGI Middleware] Response Status: {status}")
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
