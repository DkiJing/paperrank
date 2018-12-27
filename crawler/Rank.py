

class Rank(object):
    def __init__(self,List):
        self.List = List

    def getScoreList(self):
        min_ = min(self.List)
        max_ = max(self.List)
        scorelist = []
        if (max_ == min_):
            for i in self.List:
                score = 100
                scorelist.append(score)
        else:
            for i in self.List:
                score = (i - min_) / (max_ - min_) * 100
                scorelist.append(score)
        return scorelist