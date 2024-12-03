import random

from myapp.search.objects import ResultItem, Document
from myapp.search.algorithms import search_in_corpus


# aquest metode no l'hem de fer servir - nomes carrega els resultats per la demo 
def build_demo_results(corpus: dict, search_id):
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    for index in range(random.randint(0, 40)):
        item: Document = ll[random.randint(0, size)]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


class SearchEngine:
    """educational search engine"""

    def search(self, search_query, search_id, corpus):
        print("Search query:", search_query)

        res = []
        ranked_docs, ranked_scores = search_in_corpus(search_query, 'data/index_data.pkl')
    
        for docId, score in zip(ranked_docs, ranked_scores):
            item = corpus.get(docId, None)
            
            # add the dwell time - have to compute it
            res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                           "doc_details?docId={}&search_id={}&param2=2".format(item.docId, search_id), score, docId, 
                            search_query, search_id))
        
        # simulate sort by ranking
        res.sort(key=lambda doc: doc.ranking, reverse=True)
        return res


            