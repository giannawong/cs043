import wsgiref.simple_server
import urllib.parse

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response('200 OK', headers)
    s = "environ['PATH_INFO'] = " + environ['PATH_INFO'] + "\n" +\
    "environ['QUERY_STRING'] = " + environ['QUERY_STRING'] + "\n"
    return [s.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)

parameter = urllib.parse.parse_qs('data=welcome&event=my%20party&data=pi%C3%B1ata')
print(parameter)

httpd.serve_forever()