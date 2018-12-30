from django.db import models
from crawler.indexModels import es_insert


# Create your models here.
class Author(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    name = models.CharField(null=True,max_length=250, unique=True)

    def __str__(self):
        if self.name != None:
            return self.name


    class Meta:
        managed = True
        db_table = 'author'

class Citation(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    url_id = models.CharField(unique=True, max_length=254)
    cited_times = models.IntegerField(null=True)
    source = models.CharField(null=True,max_length=254)

    class Meta:
        managed = True
        db_table = 'citation'

class Paper(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    url = models.CharField(null=True, max_length=1000)
    title = models.CharField(unique=True,max_length=254)
    date = models.IntegerField(null=True)
    source = models.CharField(null=True,max_length=100)
    publisher = models.CharField(null=True,max_length=1000)
    cited_times = models.IntegerField(null=True)
    abstract = models.CharField(null=True, max_length=7000)
    keywords =  models.CharField(null=True, max_length=7000)
    authors = models.ManyToManyField(to='Author')
    cited = models.ManyToManyField(to='Citation')


    def getPaper(self, id):
        paper = Paper.objects.get(id=id)
        authors = []
        citedlist = []
        a = paper.authors.all()
        for author in a:
            authors.append(author.name)
        c = paper.cited.all()
        for citedby in c:
            cited = {}
            cited['url_id'] = citedby.url_id
            cited['source'] = citedby.source
            cited['cited_times'] = citedby.cited_times
            citedlist.append(cited)
        info = {}
        info['url_id'] =  paper.url
        info['title'] = (paper.title)
        info['date'] = (paper.date)
        info['source'] = (paper.source)
        info['publisher'] = (paper.publisher)
        info['cited_times'] = (paper.cited_times)
        info['abstract'] = (paper.abstract)
        info['keywords'] = (paper.keywords)
        info['authors'] = (authors)
        info['citedBy'] = (citedlist)
        return info

    class Meta:
        managed = True
        db_table = 'paper'


    def insert(self, url, title, date, source, publisher, cited_times, abstract, author, keywords, citations):
        obj = Paper.objects.create( url=url, title=title, date=date, source=source, publisher=publisher, cited_times=cited_times,abstract=abstract, keywords = keywords)
        id = obj.id
        es_insert(id, title, abstract, keywords, ','.join(author))
        for person in author:
            try:
                author = Author.objects.create(name = person)
                obj.authors.add(author)
            except BaseException as e:
                es_insert(id, title, abstract, keywords.lower())
                print(e)

        for key in citations[0]:
            try:
                citation = Citation.objects.create(url_id = key, cited_times = citations[0][key], source = source )
                obj.cited.add(citation)
            except BaseException as e:
                print(e)

