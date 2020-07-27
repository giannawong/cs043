import wsgiref.simple_server


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response('200 OK', headers)

    path = environ['PATH_INFO']
    if path == '/biography':
        page = '''<!DOCTYPE html>
            <html>
                <head>
                    <meta charset='UTF-8'>
                    <title>Gianna's Biography</title>
                </head>
                <body>
                    <h1 style="color:gray">Gianna Wong's Intro</h1>
                    <h2 style="background-color:yellow">A Brief Summary</h2>
                    <p>Gianna Wong is a 16-year-old student from California.</p>
                    <img style="border:1px solid" src="https://cdn.wallpapersafari.com/69/40/0cp76g.jpg" height="150" />
                    <br><br>
                    <a href='https://www.youtube.com/watch?v=cXrc1ug28oE'>One of my young endeavors</a>
                    <br><br>Submit some input.<br>
                    <form>
                        <input type="text" name="input">
                        <input type="submit" value="Submit">
                    </form>
                </body>
            </html>'''
        return [page.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
