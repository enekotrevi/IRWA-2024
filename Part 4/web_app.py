import os
from json import JSONEncoder
import json
import re


# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
import random
from flask import Flask, render_template, session
from flask import request
from datetime import datetime, timedelta
from pytz import timezone, utc

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Document, StatsDocument, Query, Visitor, Session
from myapp.search.search_engine import SearchEngine
from myapp.core.utils import load_sessions_from_file, read_visitors_file


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our search engine
search_engine = SearchEngine()

# instantiate our in memory persistence
analytics_data = AnalyticsData()

# path 
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

# load documents corpus into memory.
file_path_data = 'data' + "/farmers-protest-tweets.json"
file_path_map = 'data' + "/tweet_document_ids_map.csv"
visitors_file = 'visitors.txt'
sessions_file = 'session_log.txt'

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path_data, file_path_map)
print("loaded corpus. first elem:", list(corpus.values())[0])

# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2024 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    # initilize context variables
    browser = agent.get('browser', {}).get('name', 'Unknown')
    OS = agent.get('os', {}).get('name', 'Unknown')
    device = 'Mobile' if 'Mobile' in user_agent else 'Desktop' 
    time_of_day = datetime.now().strftime("%H:%M:%S") 
    date = datetime.now().strftime("%Y-%m-%d") 

    # save the visitor variables 
    analytics_data.visitor = Visitor(browser, OS, device, time_of_day, date, user_ip, None, None)
    
    # add the visitor to the visitors file
    if analytics_data.visitor: 
        # writing the content to the file
        with open(visitors_file, 'a') as file:
            line = analytics_data.visitor.to_dict() 
            json.dump(line, file, indent=4)            

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)

    # sessions
    if 'session_id' not in session:
        session_id = random.randint(1000, 9999)
        session['session_id'] = session_id
        session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_data = {
            'session_id': session.get('session_id'),
            'start_time': session.get('start_time'),
            'some_var': session.get('some_var')
        }
        with open(sessions_file, 'a') as file:
            line = session_data.to_dict() 
            json.dump(line, file, indent=4)  

    analytics_data.http_analytics.add_click("index", request.url, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']

    session['last_search_query'] = search_query
    
    if search_query not in analytics_data.queries:
        search_id = analytics_data.save_query_terms(search_query)
    else: 
        search_id = analytics_data.update_query_terms(search_query)

    # search algorithms
    results = search_engine.search(search_query, search_id, corpus)

    # number of results
    found_count = len(results)
    session['last_found_count'] = found_count

    # save the click time for query and query id in the session
    session['click_time_query'] = datetime.now()
    session['search_id'] = search_id

    print(session)

    # save the click 
    analytics_data.http_analytics.add_click("results", request.url, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # redirect to the results page
    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count, search_id=search_id)

@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')

    print("doc details session: ")
    print(session)

    res = session["some_var"]

    print("recovered var from session:", res)

    # get the query string parameters from request
    clicked_doc_id = request.args["docId"]
    p1 = int(request.args["search_id"])  # transform to Integer
    p2 = int(request.args["param2"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))

    # store the click time and clicked doc ID in session
    session['click_time'] = datetime.now()
    session['clicked_doc_id'] = clicked_doc_id

    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))

    doc: Document = corpus.get(clicked_doc_id, None)  # Ensure clicked_doc_id is an integer

    # add the click
    analytics_data.http_analytics.add_click("doc_details", request.url, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return render_template('doc_details.html', item=doc)

@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """

    clicks_data = []
    searched_queries = []

    for term, query in analytics_data.queries.items():
        searched_queries.append(query.to_json())

    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus.get(doc_id, None)
        count = analytics_data.fact_clicks[doc_id]
        doc = StatsDocument(row.id, row.docId, row.title, row.description, row.doc_date, row.url, count, row.likes, row.retweets, row.dwell_time)
        clicks_data.append(doc.to_json())

    # simulate sort by ranking
    #docs.sort(key=lambda doc: doc.count, reverse=True)

    # add the click
    analytics_data.http_analytics.add_click("stats", request.url, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Get the visitor history using the new function
    visitor_history = read_visitors_file(visitors_file)

    requests = analytics_data.http_analytics.requests
    clicks = analytics_data.http_analytics.clicks
    sessions = load_sessions_from_file(sessions_file)

    print('TYPE', type(sessions[0]))

    return render_template('stats.html', clicks_data=clicks_data, searched_queries=searched_queries, visitor_history=visitor_history,
    requests=requests, clicks=clicks, sessions=sessions)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    searched_queries = []

    for term, query in analytics_data.queries.items():
        searched_queries.append(query.to_json())

    for doc_id in analytics_data.fact_clicks.keys():

        # obtain the document 
        d: Document = corpus.get(doc_id, None)

        # revisar si cal mostrar els likes i els retweets en el graph
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id], d.likes, d.retweets, d.dwell_time, d.doc_date)        
        
        # convert the doc to json object
        visited_docs.append(doc.to_json())

    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc['counter'], reverse=True)

    for doc in visited_docs: print(doc)

    # Get the visitor history using the new function
    visitor_history = read_visitors_file(visitors_file)

    # add the click
    analytics_data.http_analytics.add_click("dashboard", request.url, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    requests = analytics_data.http_analytics.requests
    clicks = analytics_data.http_analytics.clicks
    sessions = load_sessions_from_file(sessions_file)

    print('SESSIONS', sessions)

    return render_template('dashboard.html', visited_docs=visited_docs, searched_queries=searched_queries, 
    visitor_history=visitor_history, requests=requests, clicks=clicks, sessions=sessions)

@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)

# method to track each request
@app.before_request
def track_request():
    """
    Track each HTTP request.
    """
    url = request.url
    method = request.method
    ip_address = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    analytics_data.http_analytics.add_request(url, method, ip_address, timestamp)

# method to compue the dwell time
@app.route('/save_dwell_time', methods=['GET'])
def save_dwell_time():

    # retrive the doc id and the init dwell
    clicked_doc_id = request.args.get('docId')
    dwell_init = session.get('click_time').replace(tzinfo=None)

    if clicked_doc_id and dwell_init:
        # store the actual time
        # use it to compute the dwell time
        dwell_end = datetime.now().replace(tzinfo=None)
        dwell_time = (dwell_end - dwell_init).total_seconds()
        
        #  obtain the doc 
        doc: Document = corpus.get(clicked_doc_id, None)

        # update the dwell time to the doc
        if doc:
            doc.update_dwell(dwell_time)
               
    return "", 204

# method com compute the dwell time for query 
@app.route('/save_dwell_time_query', methods=['GET'])
def save_dwell_time_query():
    """
    Calculate and save the dwell time for the query when returning to the index page.
    """
    query_id = request.args.get('search_id')
    dwell_init = session.get('click_time_query').replace(tzinfo=None)

    
    if dwell_init and query_id:
        dwell_end = datetime.now().replace(tzinfo=None)
        dwell_time = (dwell_end - dwell_init).total_seconds()

        dwell_time_query = (dwell_end - dwell_init).total_seconds()

        # obtain the query by id 
        query = analytics_data.get_query_by_id(int(query_id))  

        # update the query time
        if query: 
            query.update_dwell(dwell_time_query) 

    return "", 204

if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)