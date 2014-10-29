from bottle import run,route,get,post,request,static_file,redirect,app,template
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
import operator
from beaker.middleware import SessionMiddleware

CLIENT_ID = '395936545769-71fnqj77gtni1vflk366qv41e345jf6e.apps.googleusercontent.com'
CLIENT_SECRET = '_5cneg88pgpKmwdOixxCOoSj'
REDIRECT_URI = 'http://localhost:8080/redirect'
SCOPE = 'https://www.googleapis.com/auth/userinfo.email',

wordCountHistory = {}

#setup beaker
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

#@route('/test')
#def test():
#  s = request.environ.get('beaker.session')
#  s['test'] = s.get('test',0) + 1
#  s.save()
#  return 'Test counter: %d' % s['test']

run(app=app)

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

@get('/search')
def search():
    user_info = request.environ.get('beaker.session')
    return template('search',user=user_info)

@post('/search')
def do_search():
    #replace white space with %20
    q = "%20".join(request.forms.get('keywords').split())
    redirect('/result/{}'.format(q))

@get('/result/<q>')
def result(q):
    #recover white space from %20
    keyString = " ".join(q.split("%20"))
    wc = query(keyString)
    return wordCountHTML(wc,keyString)

@route('/login', 'GET')
def login():
    flow = flow_from_clientsecrets("client_secrets.json",
                                scope=SCOPE,
                                redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    redirect(str(uri))

@route('/redirect')
def redirect_page():
    code = request.query.get('code','')
    #change to elastic id -> redirect_uri
    #redo oauth and client
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            scope=SCOPE,
                            redirect_uri='http://localhost:8080/redirect')
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
    s.save()
    redirect('/search')

#todo: revoke auth page
@get('/logout')
def logout():
    request.environ.get('beaker.session').delete()
    redirect('/search')

@get('/query')
def queryResult():
    Top20 = getTop20(wordCountHistory)
    return top20HTML(Top20)

#count words in the input String, save to a dictionary
def query(keyString):
    wordCount = {}
    for word in keyString.split():
        word = word.lower()
        # check key
        if word in wordCount:
            wordCount[word] += 1
        else:
            wordCount[word] = 1
        # Store searching history
        global wordCountHistory
        if word in wordCountHistory:
            wordCountHistory[word] += 1
        else:
            wordCountHistory[word] = 1
    return wordCount

#**************For future use: change table style**************
def getTableHeader():
    headerFont = '''
           <head>
           <style>
                table {
                    width:20%;
                }
                table, th, td {
                    border-collapse: collapse;
                }
                th, td { padding: 5px;
                         text-align: left;
                }
                tr:nth-child(even) {
                    background-color: #ADBDCD;
                    color: white;
                }
                tr:nth-child(odd) {
                    background-color: #7F98B2;
                    color: white;
                }
                th {
                    background-color:#4D7094;
                    color: white;
                }
           </style>
           </head>
    '''
    return headerFont

def getAttributes():
    attributes = '''
                    <tr>
                        <th>{COLUMN1}</th>
                        <th>{COLUMN2}</th>
                    </tr>
    '''
    return attributes

def getRow():
    row = '''
            <tr>
                <td>{COLUMN1}</td>
                <td>{COLUMN2}</td>
            </tr>
    '''
    return row

#creating a html using the queried dictionary
def wordCountHTML(query, keyString):
    heading = '''<h2>Search for"{KEYSTRING}"</h2>'''
    tableName = '''<table id="results">'''
    #headerFont = getTableHeader()
    attributes = getAttributes().format(COLUMN1 = "Word", COLUMN2 = "Count")
    HTML = heading.format(KEYSTRING=keyString) + tableName + attributes
    row = getRow()
    for word,count in query.iteritems():
        HTML += row.format(COLUMN1=word,COLUMN2=count)
    HTML += "</table>"
    HTML += "<p><a href='/'>Back to Index</a></p>"
    return HTML

#Store all words count information since the server is started, save results in a list
def getTop20(wordCountHistory):
    sortedKW = sorted(wordCountHistory.items(), key=operator.itemgetter(1),reverse = True)
    return sortedKW[:20]

#creating a html using the sorted list
def top20HTML(top20):
    heading = '''<h2>Top 20 key words</h2>'''
    tableName = '''<table id="history">'''
    #headerFont = getTableHeader()
    attributes = getAttributes().format(COLUMN1 = "Word", COLUMN2 = "count")
    HTML = tableName + attributes
    row = getRow()
    for word,count in top20:
        HTML += row.format(COLUMN1=word,COLUMN2=count)
    HTML +="</table>"
    HTML += "<p><a href='/'>Back to Index</a></p>"
    return HTML

run(host='localhost', port=8080, debug=True)
#run(host='0.0.0.0', port=80)
