from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from crawler.crawler import crawler_offline


keyword_list = ['recognition',
                'machine+learning']

def call_crawler_offline(request):
    crawler_offline(keyword_list)
    return HttpResponse("<html><body>helloworld!</html></body>")


