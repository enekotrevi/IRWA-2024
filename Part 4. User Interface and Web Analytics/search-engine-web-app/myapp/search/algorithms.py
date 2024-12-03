import pickle
import re

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import collections
from collections import defaultdict
import numpy as np
from numpy import linalg as la
import nltk


# Functions

# pel create index no la necessitem, pero la tenim per si de cas, si no es fa servir borrar la funció
def process_tweet(tweet):
    """
    Preprocess the tweet removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.

    Argument:
    line -- string (tweet) to be preprocessed

    Returns:
    tweet - a list of tokens corresponding to the input text after the preprocessing
    """

    stemmer = PorterStemmer() # define the stemmer
    stop_words = set(stopwords.words("english")) # define the stopwords
    tweet =  tweet.lower() # transform the line to lowercase
    tweet = tweet.replace('\\n', '') # remove newline characters
    tweet = ' '.join(tweet.split()) # remove extra whitespaces
    tweet = re.sub(r'\S*https?:\S*', '', tweet) # delete URLs on the tweet because we won't be able to access to them
    tweet.strip() # remove spaces at first and at the end of a message
    tweet = re.sub(r' ?#\S+', '', tweet) # remove word that is with the hastag - hastag is saved separately
    tweet = re.sub(r'[^a-z0-9#@ ]+', '', tweet) # remove punctuation
    tweet = re.sub(r'[^\w\s]', '', tweet) # delete punctuation
    tweet = tweet.split() # tokenize the text to get a list of terms
    tweet = [word for word in tweet if word not in stop_words] # eliminate the stopwords
    tweet = [stemmer.stem(word) for word in tweet] # perform stemming

    return tweet

def create_tfidf_index(filepath):
    # create index from serialize data
    with open(filepath, 'rb') as f:
        index, tf, df, idf = pickle.load(f)

    return index, tf, df, idf

def rank_documents(terms, docs, index, idf, tf):
    """
    Perform the ranking of the results of a search based on the tf-idf weights

    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies

    Returns:
    Print the list of ranked documents
    """

    doc_vectors = defaultdict(lambda: [0] * len(terms)) # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
    query_vector = [0] * len(terms)

    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query.
    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        if term not in index:
            continue

        ## Compute tf*idf(normalize TF as done with documents)
        query_vector[termIndex]= query_terms_count[term]/ query_norm * idf[term]

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):

            #tf[term][0] will contain the tf of the term "term" in the doc 26
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]  # TODO: check if multiply for idf

    doc_scores=[[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores.sort(reverse=True)

    result_docs = [x[1] for x in doc_scores]
    result_scores = [x[0] for x in doc_scores]

    if len(result_docs) == 0:
        print('No results found, try again')
        query = input()
        docs = search_tf_idf(query, index)
    return result_docs, result_scores    


def search_tf_idf(query, index):
    """
    output is the list of documents that contain any of the query terms.
    So, we will get the list of documents for each query term, and take the union of them.
    """
    query = process_tweet(query)
    docs = set()
    for term in query:
        try:
            # store in term_docs the ids of the docs that contain "term"
            term_docs=[posting[0] for posting in index[term]]
            docs |= set(term_docs)
        except:
            #term is not in index
            pass
    docs = list(docs)
    ranked_docs = rank_documents(query, docs, index, idf, tf)
    return ranked_docs


def search_in_corpus(query, filepath):
    # revisar com es crea el metode i com es relaciona amb el search engine - potser no cal fer-lo 
    # i es pot fer tot des de la classe search engine

    # 1. create create_tfidf_index
    index, tf, df, idf = create_tfidf_index(filepath)

    # 2. search
    query = process_tweet(query)
    docs = set()
    for term in query:
        try:
            # store in term_docs the ids of the docs that contain "term"
            term_docs=[posting[0] for posting in index[term]]
            docs |= set(term_docs)
        except:
            #term is not in index
            pass
    docs = list(docs)

    # 2. apply ranking
    ranked_docs, ranked_scores = rank_documents(query, docs, index, idf, tf)

    return ranked_docs, ranked_scores
