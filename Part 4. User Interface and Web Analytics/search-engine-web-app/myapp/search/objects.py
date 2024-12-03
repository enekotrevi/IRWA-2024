import json


class Document:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, likes, retweets, url, hashtags, docId, dwell_time):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags
        self.docId = docId
        self.dwell_time = dwell_time


    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

    def update_dwell(self, dwell_time):
        self.dwell_time = dwell_time


class StatsDocument:
    """
    Original corpus data as an object
    """

    def __init__(self, id, docId, title, description, doc_date, url, count, likes, retweets, dwell_time):
        self.id = id
        self.docId = docId
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.count = count
        self.likes = likes 
        self.retweets = retweets
        self.dwell_time = dwell_time


    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
        
    def to_json(self):
        return self.__dict__


# object to data collection for queries 
# review - order
class Query:
    """
    Query data as an object
    """

    def __init__(self, id, terms, times_searched, dwell_time):
        self.terms = terms
        self.id = id
        self.length = len(terms.split())
        self.times_searched = times_searched
        self.dwell_time = dwell_time
        
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
    
    def to_json(self):
        return self.__dict__

    def update_dwell(self, dwell_time):
        self.dwell_time = dwell_time

# add dwell time
class ResultItem:
    def __init__(self, id, title, description, doc_date, url, ranking, docId, related_query, query_id):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.ranking = ranking
        self.docId = docId
        self.related_query = related_query
        self.query_id = query_id

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class Visitor:
    """
    User context as an object
    """
    def __init__(self, browser, OS, device, time_of_day, date, ip_address, country, city):
        self.browser = browser
        self.OS = OS
        self.device = device
        self.time_of_day = time_of_day
        self.date = date
        self.ip_address = ip_address
        self.country = country
        self.city = city

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

    def to_dict(self):
        return {
            'browser': self.browser,
            'OS': self.OS,
            'device': self.device,
            'time_of_day': self.time_of_day,
            'date': self.date,
            'ip_address': self.ip_address,
            'country': self.country,
            'city': self.city
        }

    def to_json(self):
        return self.__dict__

# class to store the HTTP info
class HTTPAnalytics:
    def __init__(self):
        self.requests = []  # List to store request data
        self.clicks = []  # List to store click data
        self.sessions = []  # List to store session data - com els visitors, es guarda de manera externa

    def add_request(self, url, method, ip_address, timestamp):
        request_data = {
            "url": url,
            "method": method,
            "ip_address": ip_address,
            "timestamp": timestamp
        }
        self.requests.append(request_data)

    def add_click(self, element, url, timestamp):
        click_data = {
            "element": element,
            "url": url,
            "timestamp": timestamp
        }
        self.clicks.append(click_data)

class Session:
    def __init__(self, session_id=None, start_time=None):
        self.session_id = session_id
        self.start_time = start_time

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Convert the object to a dictionary
        """
        return {
            'session_id': self.session_id,
            'start_time': self.start_time,
        }

    def to_json(self):
        """
        Convert the object to a JSON-compatible dictionary (for serialization)
        """
        return json.dumps(self.to_dict())
