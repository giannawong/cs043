import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random

connection = sqlite3.connect("users.db")
cursor = connection.cursor()
result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
r = result.fetchall()

if r == []:
    connection.execute("CREATE TABLE 'users' ('username','password')")


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute("SELECT * FROM 'users' WHERE 'username'=?", [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken. <a href="/">Create account</a>'.format(un).encode()]
        else:
            connection.execute("INSERT INTO 'users' VALUES (?, ?)", [un, pw])
            connection.commit()
            start_response('200 OK', headers)
            return ['Username {} created successfully. <a href="/account">Account</a>'.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute("SELECT * FROM 'users' WHERE 'username' = ? AND 'password' = ?", [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password <a href="/">Login</a>'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':


        if 'HTTP_COOKIE' not in environ:
            start_response('200 OK', headers)
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            start_response('200 OK', headers)
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute("SELECT * FROM 'users' WHERE 'username' = ? AND 'password' = ?", [un, pw]).fetchall()

        #This is where the game begins. This section of is code only executed if the login form works, and if the user is successfully logged in
        if user:
            correct = 0
            wrong = 0
            headers.append(('Set-Cookie', 'correct = {}'.format(correct)))
            headers.append(('Set-Cookie', 'wrong = {}'.format(wrong)))
            start_response('200 OK', headers)

            cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                cookies.load(environ['HTTP_COOKIE'])
                if 'correct' in cookies and 'wrong' in cookies:
                    correct = int(cookies['correct'].value)
                    wrong = int(cookies['wrong'].value)

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'

            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                parameter = urllib.parse.parse_qs(environ['QUERY_STRING'])
                guess = int(parameter['answer'][0])
                fac1 = int(parameter['factor1'][0])
                fac2 = int(parameter['factor2'][0])
                product = fac1*fac2
                if guess == product:
                    correct = 1 + int(cookies['correct'].value)
                    correctpage = '''<p style="background-color: lightgreen">Correct, {} x {} is {}. <a href="/account">Next</a> or <a href="/logout">Log out</a></p>'''.format(fac1, fac2, product)
                    return [correctpage.encode(), correct]
                else:
                    wrong = 1 + int(cookies['wrong'].value)
                    incorrectpage = '''<p style="background-color: red">Incorrect, {} x {} is {}. <a href="/account">Next</a> or <a href="/logout">Log out</a></p>'''.format(fac1, fac2, product)
                    return [incorrectpage.encode(), wrong]

            elif 'reset' in params:
                correct = 0
                wrong = 0

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1


            page = page + '<h1>What is {} x {}?</h1>'.format(f1, f2)

            answer = [f1*f2, random.randint(1, 101), random.randint(1, 101), random.randint(1, 101)]
            random.shuffle(answer)

            page += '''<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">A: {}</a><br>'''.format(un, pw, f1, f2, answer[0], answer[0])
            page += '''<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">B: {}</a><br>'''.format(un, pw, f1, f2, answer[1], answer[1])
            page += '''<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">C: {}</a><br>'''.format(un, pw, f1, f2, answer[2], answer[2])
            page += '''<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">D: {}</a><br>'''.format(un, pw, f1, f2, answer[3], answer[3])


            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a> or <a href="/logout">Log out</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

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
