import urllib.parse
import wsgiref.simple_server
from project_database import Simpledb


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    parameter = urllib.parse.parse_qs(environ['QUERY_STRING'])

    db = Simpledb('db.txt')

    if path == '/insert':
        db.insert(parameter['key'][0], parameter['value'][0])
        start_response('200 OK', headers)
        return ['Inserted'.encode()]
    elif path == '/select':
        s = db.select_one(parameter['key'][0])
        start_response('200 OK', headers)
        if s:
            return [s.encode()]
        else:
            return ['NULL'.encode()]
    elif path == '/delete':
        s = db.delete(parameter['key'][0])
        start_response('200 OK', headers)
        if s:
            return ['Deleted'.encode()]
        else:
            return ['NULL'.encode()]
    elif path == '/update':
        s = db.update(parameter['key'][0], parameter['value'][0])
        start_response('200 OK', headers)
        if s:
            return ['Updated'.encode()]
        else:
            return ['NULL'.encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
print("Serving on port 8000...")

httpd.serve_forever()
