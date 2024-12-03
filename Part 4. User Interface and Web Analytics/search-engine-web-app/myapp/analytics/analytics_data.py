import json
import random

from myapp.search.objects import Query, Visitor, HTTPAnalytics


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # variable to store the dwell time for each doc

    # variable to store the HTTP
    http_analytics = HTTPAnalytics()

    # visitor - user context
    visitor = None

    # dictionary to store query data by query ID and terms 
    queries = dict([])

    def save_query_terms(self, terms: str) -> int:
        """
        Save a new query with unique ID and initialize its search count to 1.
        """

        # generate a random query ID
        query_id = random.randint(0, 100000)

        # create a Query object and store it in the queries dictionary
        query_object = Query(id=query_id, terms=terms, times_searched=1, dwell_time=None)

        # save the Query object in the queries dictionary
        self.queries[terms] = query_object

        # return the query ID
        return query_id

    def update_query_terms(self, terms: str) -> int:
        """
        Update an existing query's search count by terms.
        """

        # access the query object directly
        query_object = self.queries[terms]

        # increment the times_searched
        query_object.times_searched += 1

        # return the existing query ID
        return query_object.id

    def get_query_by_id(self, query_id: int):
        """
        Retrieve a query object from analytics_data.queries using the query_id.
        """
        for query in self.queries.values():
            if query.id == query_id:
                return query
        raise ValueError(f"Query with ID {query_id} not found.")



class ClickedDoc:
    def __init__(self, doc_id, description, counter, likes, retweets, dwell_time, doc_date):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter
        self.likes = likes 
        self.retweets = retweets
        self.dwell_time = dwell_time
        self.doc_date = doc_date

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

        
