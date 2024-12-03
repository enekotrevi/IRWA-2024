import pandas as pd
import re

from myapp.core.utils import load_json_file
from myapp.search.objects import Document
from myapp.search.algorithms import process_tweet

_corpus = {}


def load_corpus(path_json, path_map) -> [Document]:

    # revisar el load json file
    """
    Load file and transform to dictionary with each document as an object for easier treatment when needed for displaying
     in results, stats, etc.
    :param path:
    :return:
    """
    
    df = _load_corpus_as_dataframe(path_json)
    df_map = pd.read_csv(path_map)
    df_map.rename(columns={'id': 'Id'}, inplace=True)

    # join both datasets in order to have the docId 
    df = df.merge(df_map, on='Id', how='left')

    # df te aquestes columns: ["Id", "Tweet", "Username", "Date", "Hashtags", "Likes", "Retweets", "Url", "Language"]
    df.apply(_row_to_doc_dict, axis=1)
    return _corpus


def _load_corpus_as_dataframe(path):
    """
    Load documents corpus from file in 'path'
    :return:
    """
    json_data = load_json_file(path)
    tweets_df = _load_tweets_as_dataframe(json_data)
    _clean_hashtags_and_urls(tweets_df)
    # Rename columns to obtain: Tweet | Username | Date | Hashtags | Likes | Retweets | Url | Language
    corpus = tweets_df.rename(
        columns={"id": "Id", "content": "Tweet", "username": "Username", "date": "Date",
                 "likeCount": "Likes",
                 "retweetCount": "Retweets", "lang": "Language"})
    # select only interesting columns
    filter_columns = ["Id", "Tweet", "Username", "Date", "Hashtags", "Likes", "Retweets", "Url", "Language"]
    corpus = corpus[filter_columns]
    return corpus


def _load_tweets_as_dataframe(json_data):
    data = pd.DataFrame(json_data)
    # parse entities as new columns
    # data = pd.concat([data.drop(['entities'], axis=1), data['entities'].apply(pd.Series)], axis=1)
    # parse user data as new columns and rename some columns to prevent duplicate column names
    data = pd.concat([data.drop(['user'], axis=1), data['user'].apply(pd.Series).rename(
         columns={"created_at": "user_created_at", "id": "user_id", "id_str": "user_id_str", "lang": "user_lang"})],
                      axis=1)
    return data


def _build_tags(row):
    tags = ' '.join(re.findall(r'#\w+', row))
    # for ht in row["hashtags"]:
    #     tags.append(ht["text"])
    # for ht in row:
    #     tags.append(ht['text'])
    return tags


# Agafa be el url
def _build_url(row):
    url = ""
    try:
        #url = row["url"][0] # tweet URL
        url = row["url"].iloc[0]  
    except:
        try:
            #url = row["url"][1] # review 
            url = row["url"].iloc[1]  
        except:
            url = ""
    return url


def _clean_hashtags_and_urls(df):
    df["Hashtags"] = df["content"].apply(_build_tags)
    # la URL no l'agafa bé 
    df["Url"] = df.apply(lambda row: _build_url(row), axis=1)
    # df["Url"] = "TODO: get url from json"
    # df.drop(columns=["entities"], axis=1, inplace=True)


def load_tweets_as_dataframe2(json_data):
    """Load json into a dataframe

    Parameters:
    path (string): the file path

    Returns:
    DataFrame: a Panda DataFrame containing the tweet content in columns
    """
    # Load the JSON as a Dictionary
    tweets_dictionary = json_data.items()
    # Load the Dictionary into a DataFrame.
    dataframe = pd.DataFrame(tweets_dictionary)
    # remove first column that just has indices as strings: '0', '1', etc.
    dataframe.drop(dataframe.columns[0], axis=1, inplace=True)
    return dataframe


def load_tweets_as_dataframe3(json_data):
    """Load json data into a dataframe

    Parameters:
    json_data (string): the json object

    Returns:
    DataFrame: a Panda DataFrame containing the tweet content in columns
    """

    # Load the JSON object into a DataFrame.
    dataframe = pd.DataFrame(json_data).transpose()

    # select only interesting columns
    filter_columns = ["id", "full_text", "created_at", "entities", "retweet_count", "favorite_count", "lang"]
    dataframe = dataframe[filter_columns]
    return dataframe


def _row_to_doc_dict(row: pd.Series):
    _corpus[row['docId']] = Document(row['Id'], row['Tweet'][0:100], row['Tweet'], row['Date'], row['Likes'],
                                  row['Retweets'],
                                  row['Url'], row['Hashtags'], 
                                  row['docId'], None)