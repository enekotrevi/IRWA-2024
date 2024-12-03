import datetime
import json
from random import random
import re
import datetime
from datetime import datetime



from myapp.search.objects import Document, StatsDocument, Query, Visitor, Session

from faker import Faker

fake = Faker()

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


def load_json_file(path):
    """Load JSON content from file in 'path'

    Parameters:
    path (string): the file path

    Returns:
    JSON: a JSON object
    """

    # original functio
    json_object = []
    with open(path) as fp:
        text_data = fp.readlines()
    
    text_data = [t.strip().replace(' +', ' ') for t in text_data]
    for t in text_data:
    # Parse the string into a JSON object
        json_data = json.loads(t)
        json_object.append(json_data)
    return json_object


def load_sessions_from_file(file_path):
    sessions = []

    with open(file_path, 'r') as file:

        file_content = file.read()
        file_content = file_content.replace('\n', '')  
        
        # extract all JSON entries from the file
        entries = re.findall(r'\{.*?\}', file_content, re.DOTALL)
        
        # convert the JSON entries into dictionaries
        json_objects = [json.loads(entry) for entry in entries]

        for session_data in json_objects:
            print('session_data:', session_data)
            session = Session(
                session_id=session_data.get('session_id'), 
                start_time=session_data.get('start_time'))

            sessions.append(session.to_json())  

    return sessions

# Define the read_visitors_file
def read_visitors_file(file_path):
    """
    Reads the visitors file and returns a list of visitors as JSON objects.
    :param file_path: The path to the visitors file.
    :return: A list of visitor JSON objects.
    """
    visitor_history = []
    
    with open(file_path, 'r') as file:
        # read the entire content of the file
        file_content = file.read()
        file_content = file_content.replace('\n', '')  
        
        # extract all JSON entries from the file
        entries = re.findall(r'\{.*?\}', file_content, re.DOTALL)
        
        # convert the JSON entries into dictionaries
        json_objects = [json.loads(entry) for entry in entries]

        for visitor_data in json_objects:
            # create a Visitor instance from the JSON data
            visitor = Visitor(
                browser=visitor_data.get('browser'),
                OS=visitor_data.get('OS'),
                device=visitor_data.get('device'),
                time_of_day=visitor_data.get('time_of_day'),
                date=visitor_data.get('date'),
                ip_address=visitor_data.get('ip_address'),
                country=visitor_data.get('country'),
                city=visitor_data.get('city')
            )
            # add the visitor to the history list
            visitor_history.append(visitor.to_json())

    return visitor_history
