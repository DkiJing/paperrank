# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# Create your models here.
from django.db import models

class Author(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    acdemic_unit = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        managed = True
        db_table = 'author'

    @classmethod
    def insert(self, firstName, lastName, Unit):
        obj = Author(id=id, first_name=firstName, last_name=lastName, acdemic_unit=Unit)
        obj.save()

    @classmethod
    def getName(self, id):
        obj = Author.objects.get(id=id)
        return str(obj.first_name) + ' ' + str(obj.last_name)

    @classmethod
    def getUnit(self, id):
        obj = Author.objects.get(id=id)
        return str(obj.acdemic_unit)

    @classmethod
    def getAuthorid(self, firstName, lastName):
        obj = Author.objects.get(first_name=firstName, last_name=lastName)
        return obj.id

class Paper(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    url = models.CharField(null=True, max_length=1000)
    title = models.CharField(max_length=300)
    date = models.IntegerField(null=True)
    field = models.CharField(null=True,max_length=100)
    publisher = models.CharField(null=True,max_length=1000)
    cited_times = models.IntegerField(null=True)
    abstract = models.CharField(null=True, max_length=8000)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'paper'

    @classmethod
    def insert(self, url, title, date, field, publisher, cited_times, abstract):
        obj = Paper(id=id, url=url, title=title, date=date, field=field, publisher=publisher, \
                    cited_times=cited_times, abstract=abstract)
        obj.save()

    @classmethod
    def getTitle(self, id):
        obj = Paper.objects.get(id=id)
        return str(obj.title)

    @classmethod
    def getUrl(self, id):
        obj = Paper.objects.get(id=id)
        return str(obj.url)

    @classmethod
    def getDate(self, id):
        obj = Paper.objects.get(id=id)
        return str(obj.date)

    @classmethod
    def getField(self, id):
        obj = Paper.objects.get(id=id)
        return str(obj.field)

    @classmethod
    def getPublisher(self, id):
        obj = Paper.objects.get(id=id)
        return str(obj.publisher)

    @classmethod
    def getCitedtimes(self, id):
        obj = Paper.objects.get(id=id)
        return str(obj.cited_times)

class PaperAuthor(models.Model):
    paperid = models.ForeignKey(Paper, models.DO_NOTHING, db_column='paperid', primary_key=True)
    authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='authorid')
    author_type = models.CharField(null=True, max_length=1000)

    class Meta:
        managed = True
        db_table = 'paper_author'
        unique_together = (('paperid', 'authorid'),)

    @classmethod
    def insert(self, paperid, authorid, authortype):
        paper = Paper.objects.get(id=paperid)
        author = Author.objects.get(id=authorid)
        paper.paperauthor_set.create(paperid=paper, authorid=author, author_type=authortype)

    @classmethod
    def getAuthorType(self, authorid):
        obj = PaperAuthor.objects.get(authorid=authorid)
        return str(obj.author_type)
