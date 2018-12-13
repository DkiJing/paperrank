from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# import request
# from urllib.request import urlopen
import bs4
import re
from crawler.models import Paper, Author
from selenium import webdriver
import time

keyword_list = ['network']


def openpage(keyword_list):
    keyword = ''
    ieee_url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=' + keyword + '&highlight=true&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals%20.AND.%20Magazines&refinements=ContentType:Early%20Access%20Articles&returnFacets=ALL&ranges=' + '2017' + '_' + '2018' + '_Year'
    acm_url = 'https://dl.acm.org/results.cfm?query=' + keyword + '&Go.x=0&Go.y=0'
    browser = webdriver.Chrome()
    browser.get(ieee_url)
    time.sleep(7)
    for keyword in keyword_list:
        year = 2018
        page = 0
        for i in range(5):
            ieee_url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=' + keyword + '&highlight=true&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals%20.AND.%20Magazines&refinements=ContentType:Early%20Access%20Articles&returnFacets=ALL&ranges=' + str(
                year - 2) + '_' + str(year) + '_Year'
            acm_url = 'https://dl.acm.org/results.cfm?query=' + keyword + '&start=' + str(
                page) + '&filtered=&within=owners%2Eowner%3DHOSTED&dte=&bfr=&srt=%5Fscore'
            browser.get(ieee_url)
            time.sleep(5)
            html = browser.page_source
            # print(html,end='############################################################\n')
            get_papers_briefInfo_from_page_ieee(html)
            browser.get(acm_url)
            time.sleep(5)
            html = browser.page_source
            get_papers_briefInfo_from_page_acm(html)
            year = year - 2
            page = page + 20
    # browser.get(url)

    # time.sleep(10)

    browser.close()
    # soup = bs4.BeautifulSoup(html, features='lxml')
    # print(soup.prettify())
    # file = open("C://Users//jianer//Desktop//texthtml.html",'r').read()


def index(request):
    query = 'recognition'
    url = url = 'https://dl.acm.org/results.cfm?query=' + query + '&Go.x=0&Go.y=0'
    openpage(keyword_list)
    return HttpResponse("<html><body>helloworld!</html></body>")


def get_papers_briefInfo_from_page_acm(html):
    # browser = webdriver.Chrome()
    # outpages = []
    # url = 'https://dl.acm.org/results.cfm?query=' + query + '&Go.x=0&Go.y=0'
    # browser.get(url)
    # html = browser.page_source
    out_soup = bs4.BeautifulSoup(html, 'lxml')
    title = None
    inpage_url = None
    authors = None
    source = None
    date = None
    field = None
    publisher = None
    cited_times = None
    abstract = None
    for detail in out_soup.find_all('div', class_='details'):
        outpage = {}
        try:
            title = "".join(detail.find('div', class_='title').text.split('\n')).strip()
            for a in detail.find('div', class_='title').find_all('a', href=True):
                inpage_url = 'https://dl.acm.org/citation.cfm?id=' + re.sub("\D", "", a['href'])
            authors = "".join(detail.find('div', class_='authors').text.split('\n')).strip().split(',')
            source = detail.find('div', class_='source')
            try:
                date = int(re.sub("\D", "", source.find('span', class_='publicationDate').text))
            except:
                print('Date can not convert to type int.')
            publisher = "".join(source.find('span', class_=None).text.split('\n')).strip()
            rank_data = detail.find('div', class_='metrics')
            ran_col2 = rank_data.find('div', class_='metricsCol2')
            try:
                cited_times = int(
                    ''.join(ran_col2.div.find('span', class_='citedCount').text.split()).split(':')[1])
            except:
                print('Cited times can not convert to type int.')
            abstract = detail.find('div', class_='abstract').text.split('\n')[1]
            field = "".join(detail.find('div', class_='publisher').text.split()).split(':')[1]
        except:
            pass
        outpage['title'] = title
        outpage['url'] = inpage_url
        outpage['date'] = date
        outpage['field'] = field
        outpage['publisher'] = publisher
        outpage['authors'] = authors
        outpage['cited_times'] = cited_times
        outpage['abstract'] = abstract
        print(outpage)
        # Insert in this line
        Paper.insert(Paper, outpage['url'], outpage['title'], outpage['date'], outpage['field'], \
                     outpage['publisher'], outpage['cited_times'], outpage['abstract'], outpage['authors'])

    # There is a problem on authors


def get_papers_briefInfo_from_page_ieee(html):
    soup = bs4.BeautifulSoup(html, features='lxml')

    for maintext in soup.find_all('div', class_='main-section'):
        print("$!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        print("get in ieee\n")
        counter = 0
        # print(maintext.find_all('div', class_='List-results-items'))
        for paper in maintext.find_all('div', class_='List-results-items'):
            document_link = ''
            title = ''
            ieeeauthor = []
            publish_on = ''
            publish_on_link = ''
            details = []
            print("get results\n")
            if (counter == 0):
                document_link = "https://ieeexplore.ieee.org" + paper.a['href']
                # print(document_link)

                # title
                titlelist = paper.a.text.split('\n')
                title = ''
                for s in titlelist:
                    if (s.strip()):
                        title += s.strip() + ' '
                # print(title)

                # authors
                ieeeauthor = paper.find_all('p', class_='author')[0].text.split(';')
                i = 0
                for person in ieeeauthor:
                    person = person.replace('\n', '')
                    person = person.strip()
                    author = person.split(' ')
                    ieeeauthor[i] = author
                    i += 1
                # print(ieeeauthor)

                # description
                description = paper.find('div', class_='description')

                # publish_on
                publish_on_list = description.a.text.split('\n')
                # publish_on = ''
                # print(publish_on_list)
                for c in publish_on_list:
                    if (c.strip()):
                        publish_on += c.strip() + ' '
                # print(publish_on)
                # publish_on_link
                publish_on_link = description.a["href"]
                # print(publish_on_link)
                # year/pages/cite/conference
                details = description.find_all('div')
                i = 0
                for context in details:
                    details[i] = context.text.replace('\n', '').replace(' ', '')
                    i += 1
                # print(details)
                # url, title, date, field, publisher, cited_times,issn, pages, sponsored
                details_dic = {}
                details_dic['Year'] = None
                details_dic['Citedby'] = None
                details_dic['Pages'] = None

                for text in details[:-1]:
                    # if text.split(":")[0] == 'Citedby':
                    #     details_dic[text.split(":")[0]]=re.sub("\D", "", text.split(':')[1])
                    # else:
                    details_dic[text.split(":")[0].replace('\t', '')] = text.split(":")[1].replace('\t', '')
                details_dic["publisher"] = details[-1]
                # print(details_dic) # string
                # abstrsct
                abstractlist = paper.find('div',
                                          class_="js-displayer-content u-mt-1 stats-SearchResults_DocResult_ViewMore hide")
                abstract = ''
                for str in abstractlist.text.split('\n'):
                    if (str.strip() != '' and str.strip() != 'View more'):
                        abstract += str.strip() + ' '
                # print(abstract)

                # print("!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5\n")
                # counter += 1
                # print(re.sub("\D", "", details[2].split(':')[1]))
                try:
                    details_dic['Year'] = re.findall(re.compile('\d{4}'), details_dic['Year'])
                    details_dic['Year'] = int(details_dic['Year'][0])
                except:
                    details_dic['Year'] = None
                try:
                    citation = re.findall(re.compile('Papers\(\d{1,}\)'), details_dic['Citedby'])
                    # print(citation)
                    details_dic['Citedby'] = re.sub("\D", "", citation[0])
                    details_dic['Citedby'] = int(details_dic['Citedby'])
                except:
                    details_dic['Citedby'] = None
                try:
                    details_dic['Pages'] = re.findall(re.compile('\d{1,}-\d{1,}'), details_dic['Pages'])
                except:
                    details_dic['Pages'] = None
                # print(details_dic['Year'])
                # print(details_dic['Citedby'])
                # print(details_dic['Pages'])
                Paper.insert(Paper, document_link, title, details_dic['Year'], 'IEEE', publish_on,
                             details_dic['Citedby'],
                             abstract, ieeeauthor)
                # url, title, date, field, publisher, cited_times
                print("after insert")


def test():
    url = ' http://en.szdnet.org.cn:1701/primo_library/libweb/action/search.do?frbg=&&indx=1&fn=search&dscnt=1&scp.scps=scope:(%22SZDNET%22),scope:(%22CUHKSZ%22),primo_central_multiple_fe&vid=szdnet&mode=Basic&ct=search&srt=rank&tab=default_tab&vl(2694827UI1)=conference_proceedings&dum=true&vl(freeText0)=recognition&dstmp=1544604074390&vid=szdnet&backFromPreferences=true'
    browser = webdriver.Chrome()
    browser.get(url)
    print(browser.page_source)


def get_paper_details_from_page_ieee(html):
    soup = bs4.BeautifulSoup(html, features='lxml')
    main_section = soup.find('div', class_="document-main-left-trail-content")
    print(main_section.prettify())

# if __name__ == '__main__':
#     file = open("C://Users//jianer//Desktop//texthtml.html", 'r').read()
#     get_papers_briefInfo_from_page_ieee(file)
