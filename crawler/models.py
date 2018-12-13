from django.db import models

# Create your models here.
class Author(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    first_name = models.CharField(null=True,max_length=1000)
    last_name = models.CharField(null=True,max_length=1000)
    # test = models.CharField(null=True,max_length=1000)
    # name = models.CharField(max_length=1000)
    # acdemic_unit = models.CharField(max_length=1000, blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'author'

    # @classmethod
    # def insert(self, firstName, lastName, Unit):
    #     id = Author.objects.latest('id').id + 1
    #     obj = Author(id=id, first_name=firstName, last_name=lastName, acdemic_unit=Unit)
    #     obj.save()

class Paper(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    url = models.CharField(null=True, max_length=1000)
    title = models.CharField(max_length=300)
    date = models.IntegerField(null=True)
    field = models.CharField(null=True,max_length=100)
    publisher = models.CharField(null=True,max_length=1000)
    cited_times = models.IntegerField(null=True)
    # isbn = models.CharField(null=True,db_column='ISBN', max_length=100)  # Field name made lowercase.
    # pages = models.CharField(null=True,max_length=100)
    # sponsored = models.CharField(null=True,db_column='Sponsored', max_length=100)  # Field name made lowercase.
    abstract = models.CharField(null=True, max_length=8000)
    authors = models.ManyToManyField(to='Author')
    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'paper'


    def insert(self, url, title, date, field, publisher, cited_times,abstract,author):
        # id = Paper.objects.latest('id').id + 1
        obj = Paper.objects.create( url=url, title=title, date=date, field=field, publisher=publisher, cited_times=cited_times,abstract=abstract)
        for person in author:
            author = Author.objects.create(first_name = person[0],last_name = person[1])
            obj.authors.add(author)



# class PaperAuthor(models.Model):
#     paperid = models.ForeignKey(Paper, models.DO_NOTHING, db_column='paperid', primary_key=True)
#     authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='authorid')
#     author_type = models.CharField(null=True,max_length=1000)
#
#     class Meta:
#         managed = True
#         db_table = 'paper_author'
#         unique_together = (('paperid', 'authorid'),)
#
#     # @classmethod
#     def insert(self, paperid, authorid, authortype):
#         paper = Paper.objects.get(id=paperid)
#         author = Author.objects.get(id=authorid)
#         paper.paperauthor_set.create(paperid=paper, authorid=author, author_type=authortype)
