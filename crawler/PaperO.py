from crawler.models import Paper as mp
url_head = {'ACM':'https://dl.acm.org/citation.cfm?id=','IEEE':'https://ieeexplore.ieee.org/document/'}
class PaperO(object):

    def __init__(self, id, url_id, title, date, \
                 source, publisher, cited_times, \
                 abstract, keywords, authors, citedBy):
        self.id = id
        self.title = title
        self.date = date
        self.source = source
        self.publisher= publisher
        self.cited_times = cited_times
        self.keywords = keywords
        self.authors = ', '.join(authors)
        self.citedBy = citedBy
        self.url_id = url_head[self.source] + url_id
        if abstract == None:
            self.abstract = '...'
        else:
            self.abstract = abstract
        # self.url = url_head[self.source] + self.url_id


def createPaper(id):
    p = mp.getPaper(mp,id)
    paper = PaperO(id,p['url_id'], p['title'], p['date'], p['source'],\
                      p['publisher'], p['cited_times'], p['abstract'],\
                      p['keywords'], p['authors'], p['citedBy'])
    if(p['date'] == 1989):
        print('############################')
        print(paper.keywords)
    return paper
