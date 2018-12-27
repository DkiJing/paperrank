import re
import time
from selenium import webdriver
import bs4
from crawler.models import Paper,Author


def crawler_offline(keyword_list):
    keyword = ''
    browser = webdriver.Chrome()
    for keyword in keyword_list:
        year = 2018
        page = 1420
        acm_url = 'https://dl.acm.org/results.cfm?query=recognition&Go.x=0&Go.y=0'
        # browser.get(acm_url)
        # time.sleep(3)
        for i in range(3):
            print(i)
            ieee_url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=' \
                       + keyword \
                       + '&highlight=true&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals%20.AND.%20Magazines&refinements=ContentType:Early%20Access%20Articles&returnFacets=ALL&ranges=' \
                       + str(year - 2) + '_' + str(year) + '_Year'
            acm_url = 'https://dl.acm.org/results.cfm?query=' + keyword + '&start=' + str(page) \
                      + '&filtered=&within=owners%2Eowner%3DHOSTED&dte=&bfr=&srt=citedCount'


            print(ieee_url)
            browser.get(ieee_url)
            time.sleep(5)
            html = browser.page_source
            get_papers_ieee(html)
            print(acm_url)
            browser.get(acm_url)
            time.sleep(5)
            html = browser.page_source
            get_papers_acm(html)
            year = year - 2
            page = page + 1000
    browser.close()

def get_each_citations_ieee(paperId,browser):
    titlelist = {}
    citationlist = {}
    url = 'https://ieeexplore.ieee.org/document/' + paperId + '/citations?tabFilter=papers#citations'
    browser.get(url)
    time.sleep(3)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, features='lxml')
    section = soup.find('div', id = 'anchor-paper-citations-ieee')
    # print(section)
    try:
        section = section.find_all('div', class_ = 'reference-container')
        for citation in section:
            title = citation.div.div.find(class_='description').text
            title = re.findall(re.compile('"(.*?)"'), title)
            # print(title)
            # print('!!!!!!!!!!!!!!!!!')
            id = citation.a['href'].split('/')[-1]
            try:
                titlelist[id] = title
                url = 'https://ieeexplore.ieee.org/document/' + id
                browser.get(url)
                time.sleep(5)
                html = browser.page_source
                soup = bs4.BeautifulSoup(html, features='lxml')
                try:
                    citenum = soup.find('div', class_='document-banner-metric-count').text
                    citationlist[id] = int(citenum)
                except:
                    citationlist[id] = 0
                    print('citenum = 0')
            except  BaseException as e:
                print(e)
    except BaseException as e:
        print(e)
    print(citationlist,titlelist)
    return citationlist, titlelist


def get_keywords_ieee(paperId,browser):
    keystring = ''
    url = 'https://ieeexplore.ieee.org/document/'+paperId + '/keywords#keywords'
    print(url)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, features='lxml')
    section = soup.find('div', class_ = 'stats-keywords-container')
    try:
        sectionlist = section.li.ul.text.split(',')
        for i in range(len(sectionlist)):
            sectionlist[i] = sectionlist[i].replace('\n','').replace('\t','')
            keystring += sectionlist[i]+' '
    except BaseException as e:
        print(e)
    # print(sectionlist)
    return keystring


def get_citation_count_acm(id,browser):
    print('incountpage')
    cita_dic = {}
    title_dic = {}
    citation_count = 0
    title = None
    in_url = 'https://dl.acm.org/citation.cfm?id=' + str(id)
    browser.get(in_url)
    time.sleep(1)
    html = browser.page_source
    in_soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        divmain = in_soup.find('div', id="divmain")
        table = divmain.table
        title = divmain.h1.text
        title_dic[id] = title
        for tr in table.find_all('tr',):
            td = tr.find_all('td')
        try:
            citation_count = int(td[-1].text.split('\n')[1].split(':')[1])
            cita_dic[id] = citation_count
        except:
            print('Citation count can not be converted to int')
    except BaseException as e:
        print(e)
    return title, citation_count

def get_each_citations_acm(id,browser):
    print('inpage')
    ref_id = 0
    cita_dic = {}
    title_dic = {}
    citation_url = 'https://dl.acm.org/tab_citings.cfm?id=' + str(id) + '&usebody=tabbody&_cf_containerId=cf_layoutareacitedby&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=3AE209A182AC2ACBEF2EB36F02A056FC&_cf_rc=1'
    browser.get(citation_url)
    time.sleep(1)
    html = browser.page_source
    citation_soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        table = citation_soup.find('table')
        for tr in table.find_all('tr',):
            td = tr.find_all('td')
            for a in td[1].find_all('a', href=True):
                ref_id = re.sub("\D", "", a['href'])
                title, citation_count = get_citation_count_acm(ref_id,browser)
                title_dic[ref_id] = title
                cita_dic[ref_id] = citation_count
    except BaseException as e:
        print(e)
    return cita_dic, title_dic


def get_papers_acm(html):
    browser = webdriver.Chrome()
    # outpages = {}
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
    key_words = None
    for detail in out_soup.find_all('div', class_='details'):
        outpage = {}
        try:
            title = "".join(detail.find('div', class_='title').text.split('\n')).strip()
            for a in detail.find('div', class_='title').find_all('a', href=True):
                inpage_url = re.sub("\D", "", a['href'])
            authors = "".join(detail.find('div', class_='authors').text.split('\n')).strip().split(',')
            # for i in range(len(authors)):
            #     authors[i] = authors[i].split(' ')
            source = detail.find('div', class_='source')
            try:
                date = int(re.sub("\D", "", source.find('span', class_='publicationDate').text))
            except BaseException as e:
                print(e)
            publisher = "".join(source.find('span', class_=None).text.split('\n')).strip()
            rank_data = detail.find('div', class_='metrics')
            ran_col2 = rank_data.find('div', class_='metricsCol2')
            try:
                cited_times = int(
                    ''.join(ran_col2.div.find('span', class_='citedCount').text.split()).split(':')[1])
            except BaseException as e:
                print(e)
            key_words = detail.find('div', class_='kw').text.split(':')[1].replace(',',' ').replace('\n','')
            abstract = detail.find('div', class_='abstract').text.split('\n')[1]
            field = "".join(detail.find('div', class_='publisher').text.split()).split(':')[1]
        except BaseException as e:
            print(e)
        outpage['title'] = title
        outpage['url'] = inpage_url
        outpage['date'] = date
        outpage['field'] = field
        outpage['publisher'] = publisher
        outpage['authors'] = authors
        outpage['cited_times'] = cited_times
        outpage['abstract'] = abstract
        outpage['kw'] = key_words
        # print(key_words)
        # print(outpage)
        # Insert in this line
        # print(authors)
        citations = get_each_citations_acm(inpage_url,browser)
        print(citations[0])
        try:
            Paper.insert(Paper, outpage['url'], outpage['title'], outpage['date'], 'ACM', \
                     outpage['publisher'], outpage['cited_times'], outpage['abstract'], outpage['authors'], outpage['kw'], citations)
            print('after insert')
        except BaseException as e:
            print(e)
    browser.close()
    # There is a problem on authors


def get_papers_ieee(html):
    browser = webdriver.Chrome()
    soup = bs4.BeautifulSoup(html, features='lxml')
    paperLinkList = []
    print("$!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    maintext = soup.find('div', class_='main-section')
    for paper in maintext.find_all('div', class_='List-results-items'):
        document_id,title, ieeeauthor, publisher, details_dic, abstract  = get_paper_ieee(paper)
        keywords = ''
        citations = {}
        keywords = get_keywords_ieee(document_id,browser)
        print(keywords)
        citations = get_each_citations_ieee(document_id,browser)
        try:
            Paper.insert(Paper, document_id, title, details_dic['Year'], 'IEEE', publisher,
                     details_dic['Citedby'],
                     abstract, ieeeauthor,keywords,citations)
            print("after insert")
        except BaseException as e:
            print(e)
        # print('after insert')
    browser.close()

def get_paper_ieee(paper):
    document_id = ''
    title = ''
    ieeeauthor = []
    publish_on = ''
    publish_on_link = ''
    details = []
    keywords = ''
    print("get in ieee\n")

    document_id = paper.a['href'].replace('/document/', '').replace('/', '')
    # print(document_id)

    ###### title
    titlelist = paper.a.text.split('\n')
    for s in titlelist:
        if (s.strip()):
            title += s.strip() + ' '
    # print(title)

    ###### authors
    ieeeauthor = paper.find_all('p', class_='author')[0].text.split(';')
    for i in range(len(ieeeauthor)):
        ieeeauthor[i] = ieeeauthor[i].replace('\n', '').strip()
    print(ieeeauthor)

    ###### description
    description = paper.find('div', class_='description')

    ### publish_on
    publish_on_list = description.a.text.split('\n')
    for c in publish_on_list:
        if (c.strip()):
            publish_on += c.strip() + ' '
    # print(publish_on)

    ### publish_on_link
    publish_on_link = description.a["href"]
    # print(publish_on_link)

    ###year/pages/cite/conference
    details = description.find_all('div')
    for i in range(len(details)):
        details[i] = details[i].text.replace('\n', '').replace(' ', '')
    # print(details)
    details_dic = {}
    details_dic['Year'] = None
    details_dic['Citedby'] = None
    details_dic['Pages'] = None
    for text in details[:-1]:
        try:
            details_dic[text.split(":")[0].replace('\t', '')] = text.split(":")[1].replace('\t', '')
        except:
            pass
    details_dic["publisher"] = details[-1]
    try:
        details_dic['Year'] = re.findall(re.compile('\d{4}'), details_dic['Year'])
        details_dic['Year'] = int(details_dic['Year'][0])
    except:
        details_dic['Year'] = None
    try:
        citation = re.findall(re.compile('Papers\(\d{1,}\)'), details_dic['Citedby'])
        details_dic['Citedby'] = re.sub("\D", "", citation[0])
        details_dic['Citedby'] = int(details_dic['Citedby'])
    except:
        details_dic['Citedby'] = 0
    try:
        details_dic['Pages'] = re.findall(re.compile('\d{1,}-\d{1,}'), details_dic['Pages'])
    except:
        details_dic['Pages'] = None
    # print(details_dic) # string

    ### abstrsct
    abstractlist = paper.find('div',
                              class_="js-displayer-content u-mt-1 stats-SearchResults_DocResult_ViewMore hide")
    abstract = ''
    for str in abstractlist.text.split('\n'):
        if (str.strip() != '' and str.strip() != 'View more'):
            abstract += str.strip() + ' '
    # print(abstract)
    return document_id, title, ieeeauthor, publish_on, details_dic, abstract