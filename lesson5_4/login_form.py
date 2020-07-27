import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies

connection = sqlite3.connect('file.db')
connection.execute('CREATE TABLE users(username, password)')
cursor = connection.cursor()


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Username already taken. Try again</p><br>
                <p>Go to <a href="/">Register</a></p>
                </body>
                </html>'''
            return [page.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            connection.commit()
            start_response('200 OK', headers)
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Username successfully registered</p><br>
                <p>Go to <a href="/account">Account</a></p>
                </body>
                </html>'''
            return [page.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Incorrect username or password</p><br>
                <p>Go to <a href="/">Log in</a></p>
                </body>
                </html>'''
            return [page.format(un).encode()]
        else:
            start_response('200 OK', headers)
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Incorrect username or password</p><br>
                <p>Go to <a href="/account">Account</a></p>
                </body>
                </html>'''
            return [page.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        page = '''<!DOCTYPE html>
            <html><head><title></title></head>
            <body><h1></h1>
            <p>Logged out</p><br>
            <p>Go to <a href="/">Log in</a></p>
            </body>
            </html>'''
        return [page.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Not logged in</p><br>
                <p>Go to <a href="/">Log In</a></p>
                </body>
                </html>'''
            return [page.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ('HTTP_COOKIE'))
        if 'session' not in cookies:
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Not logged in</p><br>
                <p>Go to <a href="/">Log In</a></p>
                </body>
                </html>'''
            return [page.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Logged in</p><br>
                <p>Go to <a href="/logout">Log out</a></p>
                </body>
                </html>'''
            return [page.format(un).encode()]
        else:
            page = '''<!DOCTYPE html>
                <html><head><title></title></head>
                <body><h1></h1>
                <p>Not logged in</p><br>
                <p>Go to <a href="/">Log In</a></p>
                </body>
                </html>'''
            return [page.encode()]

    elif path == '/':
        start_response('200 OK', headers)
        page = '''<!DOCTYPE html>
            <html><head><title></title></head>
            <body><h1></h1>
            <form action="/login" style="background-color:gold">
                <h1>Login</h1>
                Username <input type="text" name="username"><br>
                Password <input type="password" name="password"><br>
                <input type="submit" value="Log in">
            </form>
            <form action="/register" style="background-color:gold">
                <h1>Register</h1>
                Username <input type="text" name="username"><br>
                Password <input type="password" name="password"><br>
                <input type="submit" value="Register">
            </form>
            </body>
            </html>'''
        return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
