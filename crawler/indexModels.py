from elasticsearch import Elasticsearch



es = None
# if __name__ == '__main__':
es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

def es_insert(paper_id, title, abstract, keyword, author):
    body = {
        "keywords": keyword,
        "abstract": abstract,
        "title": title,
        "author": author
    }
    es.index(index='paperrank', doc_type='paper_information', id=paper_id, body=body)

def search_index(queryDict):
    print('!!!!!!')
    print(str(queryDict))
    first = queryDict.get('first')
    title = queryDict.get('Title')
    keyword = queryDict.get('Keyword')
    author = queryDict.get('Author')
    must = []
    if first is not None:
        first = first.split(" ")
        if first[0] == "Keyword":
            must = [
                {
                    "multi_match": {
                        "fields": ["keywords", "abstract"],
                        "query": first[1],
                        "fuzziness": "AUTO"
                    }
                }

            ]
        else :
            must = [{
                "match": {
                    first[0].lower(): {
                        "query": first[1],
                        "fuzziness": "AUTO",
                        "operator":  "and"
                    }
                }
            }]
    should = []
    must_not = []
    if title is not None:
        title = title.split(",")
        del title[len(title)-1]
        for T in title:
            t = T.split(" ")
            match = {
                "match": {
                    "title": {
                        "query": t[1],
                        "fuzziness": "AUTO",
                        "operator":  "and"
                    }
                }
            }
            if t[0] == "AND":
                must.append(match)
            if t[0] == "OR":
                should.append(match)
            if t[0] == "NOT":
                must_not.append(match)
    if keyword is not None:
        keyword = keyword.split(",")
        del keyword[len(keyword)-1]
        for K in keyword:
            k = K.split(" ")
            match = {
                "multi_match": {
                    "fields":  [ "keywords", "abstract" ],
                    "query":  k[1],
                    "fuzziness": "AUTO"
                }
            }
            if k[0] == "AND":
                must.append(match)
            if k[0] == "OR":
                should.append(match)
            if k[0] == "NOT":
                must_not.append(match)
    if author is not None:
        author = author.split(",")
        del author[len(author)-1]
        for A in author:
            a = A.split(" ")
            match = {
                "match": {
                    "author": {
                        "query": a[1],
                        "fuzziness": "AUTO",
                        "operator":  "and"
                    }
                }
            }
            if a[0] == "AND":
                must.append(match)
            if a[0] == "OR":
                should.append(match)
            if a[0] == "NOT":
                must_not.append(match)
    should.append({
        "bool": {
            "must": must
        }
    })
    body = {
        "query": {
            "bool": {
                "should": should,
                "must_not": must_not
            }
        },
        "size": 500
    }
    print(body)
    list = {}
    a = es.search(index='paperrank', doc_type='paper_information', body=body, filter_path=["hits.hits._id"])
    if len(a) is not 0:
        list = a.get('hits').get('hits')
    return list
