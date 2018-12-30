from django.shortcuts import render,HttpResponseRedirect,Http404,HttpResponse,render_to_response
from crawler.RankResult import getRankedList
from . import search
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

def hello(request):
    context = {}
    context['hello'] = "Hello World!"
    return  render(request,"hello.html",context)

paper_List = []
paper_List2=[]
def result(request):

    global paper_List
    global paper_List2
    mes = search.search(request)
    print('-----------------')
    print(mes)
    first = mes.get('first')
    title = ""
    keyword=""
    author=""
    date = ""
    cited = ""
    end = ""
    start = ""
    publisher = ""
    currentpage = 1
    search_condition = ""
    if "Title" in mes:
        title = "Title: " + mes.get('Title')
    if "Keyword" in mes:
        keyword ="Keyword: " + mes.get('Keyword')
    if "Author" in mes:
        author = "Author: " + mes.get('Author')
    if "date" in mes:
        date = mes.get('date')
    if "cited" in mes:
        cited = mes.get('cited')
    if "start" in mes:
        start =  mes.get('start')
    if "end" in mes:
        end = mes.get('end')
    if "publisher" in mes:
        publisher = mes.get('publisher')
    if title !=None:
        search_condition = title
    if keyword!=None:
        search_condition = search_condition + keyword
    if author!=None:
        search_condition = search_condition + author
    if "search-condition" in mes:
        search_condition = mes.get('search-condition')
    list_return = paper_List
    if end == "" and search_condition == "" or first!=None:
        paper_List = getRankedList(mes, date, cited)
        paper_List2 = getRankedList(mes, date, cited)
        print('getlist')
        list_return = paper_List2
    if date!="":
        paper_List2 = getRankedList(mes, date, cited)
        list_return = paper_List2
    if "search-condition" not in mes:
        search_condition = "Search condition: "+ first + title + keyword + author
        search_condition = str(search_condition)
    if "currentpage" in mes:
        currentpage = mes.get('currentpage')
    list2 = []
    if end!="" or start !="":
        for paper in list_return:
           if paper.date>=int(start) and paper.date<=int(end):
               if publisher != "":
                   if paper.source == publisher:
                        list2.append(paper)
               else:
                   list2.append(paper)
        list_return = list2
    paginator = Paginator(list_return,3)
    page_number = paginator.page_range
    if currentpage!="":
        try:
            contacts = paginator.page(currentpage)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
    # {"search_condition":search_condition,"date":date,"cited":cited,"start":start,"end":end,"contacts":contacts,"page_number":page_number}
    return  render_to_response("result.html",locals())
