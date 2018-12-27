# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response,render


# 表单
def search_form(request):
    ctx = {}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "search_form.html", ctx)
    #return render_to_response('search_form.html')

def js(request):
    return  render_to_response('../static/js/../templates/pk.js')

# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    message = request.GET
    Title = {}
    Keyword = {}
    Author = {}

    #if 'first' in request.GET:
    #   message = message+"first: "+ request.GET['first']
    # if 'first' in request.GET:
    #     message = message + "first: " + request.GET['first']
    # if 'Title' in request.GET:
    #     title = request.GET['Title'].split(",")
    #     for x in range(len(title)-1):
    #         data = title[x].split(" ")
    #         Title[data[1]] = data[0]
    #     message = message + "Title: " + str(Title)
    # if 'Keyword' in request.GET:
    #     keyword = request.GET['Keyword'].split(",")
    #     for x in range(len(keyword)-1):
    #         data = keyword[x].split(" ")
    #         Keyword[data[1]] = data[0]
    #     message = message + "Keyword: " + str(Keyword)
    # if 'Author' in request.GET:
    #     author = request.GET['Author'].split(",")
    #     for x in range(len(author)-1):
    #         data = author[x].split(" ")
    #         Author[data[0]] = data[1]
    #     message = message + "Author: " + str(Author)

    '''   
    if 'q' in request.GET:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    '''

    return message
    #return HttpResponse(message)


