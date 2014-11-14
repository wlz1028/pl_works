from bottle import run,route,get,post,request,static_file,redirect,app,template,error
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from mongodb import get_word_id,get_doc_ids,get_sorted_docs,get_sorted_urls
import httplib2
import operator
from beaker.middleware import SessionMiddleware
import json
import os,math

CLIENT_ID = '395936545769-71fnqj77gtni1vflk366qv41e345jf6e.apps.googleusercontent.com'
CLIENT_SECRET = '_5cneg88pgpKmwdOixxCOoSj'
REDIRECT_URI = 'http://localhost:8080/redirect'
SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

USER_HISTORY_PATH = './data/user_word_count_history.json'

#setup beaker
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)
#run(app=app)

@get('/')
def root():
    redirect('/search')

@get('/search')
def search():
    user_info = request.environ.get('beaker.session')
    if isLogin():
        topHist = getTop20(user_info['email'])
        if len(topHist) > 10:
            topHist = topHist[:10]
    else:
        topHist = []
    return template('search',user=user_info,QUERY=topHist)

@post('/search')
def do_search():
    #replace white space with %20
    q = "%20".join(request.forms.get('keywords').split())
    redirect('/result/{}/{}'.format(q,1))

#@get('/result')
#def result(q):
#    """
#    return search result HTML
#    """
#    return "please enter something"

@get('/test')
def test():
    message = '\"{}\"Cannot be found'.format(keyString)
    return template('error',ERRORMESSAGE=message)



@get('/result/<q>/<p>')
def result(q, p=1):
    """
    return search result HTML
    """
    #recover white space from %20
    keyString = " ".join(q.split("%20"))
    wc = countWord(keyString)
    first_word = keyString.split()[0]
    word_id = get_word_id(first_word)
    doc_ids = get_doc_ids(word_id)
    sorted_doc_ids = get_sorted_docs(doc_ids)
    sorted_url = get_sorted_urls(sorted_doc_ids)
    page = int(p)
    previous = page-1
    nextpage = page+1

    if page > math.ceil(len(sorted_url)/float(10)) and page!=1:
        return error404(404)
    if not sorted_url:
        message = '"{}" Cannot be found'.format(keyString)
        return template('error',ERRORMESSAGE=message)

    return template('result', KEYSTRING=keyString, URLS=sorted_url, PAGE_NUMBER=page, PREVIOUS=previous, NEXT=nextpage, USER_DISPLAY=getUserDisplay(),QUERY=q)

@get('/query')
def queryResult():
    """
    return user history page HTML
    """
    if not isLogin():
        return 'Please <a href="/login">login</a> to see your search history'
    user_info = request.environ.get('beaker.session')
    return template('user_search_history', USER_DISPLAY=getUserDisplay(), QUERY=getTop20(user_info['email']))

#@get('/error/<q>')
#def general_error(q="General error"):
#    """
#    return error message HTML
#    """
#    return "Opps!!<br>Error:{}".format(q)

#login page
@route('/login', 'GET')
def login():
    flow = flow_from_clientsecrets("client_secrets.json",
                                scope=SCOPE,
                                redirect_uri=REDIRECT_URI)
    uri = flow.step1_get_authorize_url()
    redirect(str(uri))

#login redirect
@route('/redirect')
def redirect_page():
    code = request.query.get('code','')
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            scope=SCOPE,
                            redirect_uri=REDIRECT_URI)
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']

    #get user info
    http = httplib2.Http()
    http = credentials.authorize(http)

    #Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']
    s = request.environ.get('beaker.session')
    s['email'] = user_email
    s['login'] = True
    s.save()
    redirect('/search')

#TODO: ISSUE-when user logout, and then login, no login page
@get('/logout')
def logout():
    request.environ.get('beaker.session').delete()
    redirect('/search')

@error(404)
def error404(error):
    return template('error',ERRORMESSAGE="404 Page Not Found")

#setup image fetch
@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='./images', mimetype='image/png')

#setup html fetch
@route('/<filename:re:.*\.html>')
def server_html_static(filename):
    return static_file(filename, root='./')

#setup css fetch
@route('/<filename:re:.*\.css>')
def server_css_static(filename):
    return static_file(filename, root='./')

#count words in the input String, save to a dictionary
def countWord(keyString):
    """
    return word,count dictionary
    store user search word count on disk
    """
    wordCount = {}
    for word in keyString.split():
        word = word.lower()
        # check key
        if word in wordCount:
            wordCount[word] += 1
        else:
            wordCount[word] = 1

        # Store searching history on disk in json format
        if isLogin():
            user_info = request.environ.get('beaker.session')
            storeWordCountHistory(user_info['email'], word)
    return wordCount

def storeWordCountHistory(user_email, word):
    """
    return None
    Store user history to disk
    """
    #Load or create user history json file
    try:
        with open(USER_HISTORY_PATH, 'r+') as f:
            history = json.load(f)
    except:
        with open(USER_HISTORY_PATH, 'w') as f:
            history = {}

    #update user history file
    with open(USER_HISTORY_PATH, "w") as f:
        if not user_email in history:
            history[user_email] = {}
        if word in history[user_email]:
            history[user_email][word] += 1
        else:
            history[user_email][word] = 1
        json.dump(history,f,indent=4)

def get_user_history(user_email):
    """
    return user history disctionary
    return {} if user history not found on disk
    """
    try:
    	with open(USER_HISTORY_PATH, 'r') as f:
    	    history = json.load(f)
    except:
	return {}

    if user_email in history:
        return history[user_email]
    else:
        return {}


#Pretty table
#def getTableHeader():
#    headerFont = '''
#           <head>
#           <style>
#                table {
#                    width:20%;
#                }
#                table, th, td {
#                    border-collapse: collapse;
#                }
#                th, td { padding: 5px;
#                         text-align: left;
#                }
#                tr:nth-child(even) {
#                    background-color: #ADBDCD;
#                    color: white;
#                }
#                tr:nth-child(odd) {
#                    background-color: #7F98B2;
#                    color: white;
#                }
#                th {
#                    background-color:#4D7094;
#                    color: white;
#                }
#           </style>
#           </head>
#    '''
#    return headerFont

def getTop20(user_email):
    """
    return user top 20 word count history
    """
    user_history = get_user_history(user_email)
    sortedKW = sorted(user_history.items(), key=operator.itemgetter(1),reverse = True)
    return sortedKW[:20]

def getUserDisplay():
    """
    return user information HTML
    """
    user_info = request.environ.get('beaker.session')
    try:
        display = user_info['email'] + ' <a href="/logout">logout</a><br>'
    except:
        display = 'Anonymous can <a href="/login">login</a><br>'
    return display

def isLogin():
    """
    return true if current user if login, false otherwise
    """
    try:
        if request.environ.get('beaker.session')['login']:
            return True
        else:
            return False
    except:
        return False

run(app, host='localhost', port=8080, debug=True)
run(
        app,                    # Run |app| Bottle() instance
        host     = '0.0.0.0',
        port     = 8080,
        reloader = True,        # restarts the server every time edit a module file
#        debug    = True         # Comment out it before deploy
        )
