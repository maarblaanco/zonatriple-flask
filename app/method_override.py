from urllib.parse import parse_qs
from io import BytesIO
from werkzeug.formparser import parse_form_data


class MethodOverrideMiddleware:
    allowed_methods = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH'}

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ.get('REQUEST_METHOD', '').upper() == 'POST':
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError, TypeError):
                request_body_size = 0

            body = environ['wsgi.input'].read(request_body_size)
            environ['wsgi.input'] = BytesIO(body)

            content_type = environ.get('CONTENT_TYPE', '')
            method = ''

            if 'multipart/form-data' in content_type:
                environ_copy = dict(environ)
                environ_copy['wsgi.input'] = BytesIO(body)

                _, form, _ = parse_form_data(environ_copy, silent=True)
                method = (form.get('_method') or '').upper() if form else ''

            else:
                form_data = parse_qs(body.decode('utf-8', errors='ignore'))
                method = (form_data.get('_method', [''])[0] or '').upper()

            if method in self.allowed_methods:
                environ['REQUEST_METHOD'] = method

            environ['wsgi.input'].seek(0)

        return self.app(environ, start_response)