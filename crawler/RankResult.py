from crawler.PaperO import createPaper
from crawler.indexModels import search_index
# from crawler.DateRank import DateRank
# from crawler.CitedByRank import CitedByRank
# from crawler.CitedTimesRank import CitedTimesRank
# from crawler.SourceRank import SourceRank
de_idList = []
def getRankedList(mes, date, citedtimes):
    global de_idList
    if(mes.get('first')):
        idList = search_index(mes)
        de_idList = idList
    else:
        idList = de_idList
    print('!!!!!!!!!!!!!!!!!!!!!!')
    print(idList)
    paperList = []
    defoult_para = {}
    defoult_para = judgeDC(date, citedtimes)

    for idDic in idList:
        id = idDic['_id']
        paperList.append(createPaper(id))

    date_list = []
    citedtimes_list = []
    citedBy_list = []
    source_list = []

    for paper in paperList:
        date_list.append(paper.date)
        citedtimes_list.append(paper.cited_times)
        source_list.append(paper.source)
        sum_citedBy = 0
        for p in paper.citedBy:
            sum_citedBy += p['cited_times']
        citedBy_list.append(sum_citedBy)
    # print(date_list)
    # date_grade = DateRank(date_list).getScoreList()  # {}
    # citedtimes_grade = CitedTimesRank(citedtimes_list).getScoreList()
    # citedBy_grade = CitedByRank(citedBy_list).getScoreList()
    # source_grade = SourceRank(source_list).getScoreList()
    date_grade = getDateScoreList(date_list)  # {}
    citedtimes_grade = getCitedTimesScoreList(citedtimes_list)
    citedBy_grade = getCitedByScoreList(citedBy_list)
    source_grade = getSourceScoreList(source_list)

    d = defoult_para['date']
    cs = defoult_para['citedtimes']
    cy = defoult_para['citedBy']
    se = defoult_para['source']
    finalScore = {}
    for i in range(len(date_grade)):
        score = d * date_grade[i] + cs * citedtimes_grade[i] + cy * citedBy_grade[i] + se * source_grade[i]
        finalScore[i] = -score
    finalRank =  sorted(finalScore.items(),key = lambda x:x[1])
    print(defoult_para)
    print(finalRank)

    finalList = []
    for t in finalRank:
        finalList.append(paperList[t[0]])
    # print(finalList)
    return finalList

def judgeDC(date, citedtimes):
    # print(citedtimes)
    default_para = {'date': 1.5, 'citedtimes': 4, 'citedBy': 3, 'source': 1.5}
    if date == '100':
        default_para = {'date': 1, 'citedtimes': 0, 'citedBy': 0, 'source': 0}

    elif citedtimes == '100':
        default_para = {'date': 0, 'citedtimes': 1, 'citedBy': 0, 'source': 0}

    elif date == '' or citedtimes == '' :
        return default_para
    else:
        # print(date)
        total = 5
        date = int(date)
        citedtimes = int(citedtimes)
        date_rate = date/(date+citedtimes)
        cited_rate = citedtimes/(date+citedtimes)
        default_para = {'date': total*date_rate, 'citedtimes': total*cited_rate, 'citedBy': 3, 'source': 1.5}
        #how to adjust
    return default_para


#
def getDateScoreList(datelist):
    min_ = min(datelist)
    max_ = max(datelist)
    scorelist = []
    if ( max_  ==  min_):
        for i in datelist:
            score = 100
            scorelist.append(score)
    else:
        for i in datelist:
            score = (i - min_)/(max_ - min_)*100
            scorelist.append(score)
    return scorelist


def getCitedTimesScoreList(citedTimeslist):
    min_ = min(citedTimeslist)
    max_ = max(citedTimeslist)
    scorelist = []
    if ( max_  ==  min_):
        for i in citedTimeslist:
            score = 100
            scorelist.append(score)
    else:
        for i in citedTimeslist:
            score = (i - min_)/(max_ - min_)*100
            scorelist.append(score)
    return scorelist

def getCitedByScoreList(citedBylist):
    min_ = min(citedBylist)
    max_ = max(citedBylist)
    scorelist = []
    if ( max_  ==  min_):
        for i in citedBylist:
            score = 100
            scorelist.append(score)
    else:
        for i in citedBylist:
            score = (i - min_)/(max_ - min_)*100
            scorelist.append(score)
    return scorelist

def getSourceScoreList(sourcelist):
    result = []
    for i in range(len(sourcelist)):
        result.append(100)
    return result