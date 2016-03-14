from brightCrawler import Fetcher
from bs4 import BeautifulSoup
import re
import string
import brightParam as param
import brightUtil as util

class Page:
    def __init__(self, url, content):
        self.content = content
        self.pageObj = None
        self.outLink = []
        self.metaKey = ''
        self.title = ''
        self.metaDesc = ''
        self.__getPageObject()

    def __fill_details(self):
        #1. Get meta data details
        #Extracting description
        try:
            obj = self.pageObj.findAll(attrs=param.METATAG['DESC'])
            if obj:
                self.metaDesc = obj[0]['content']
        except KeyError:
            pass
        
        #extracting keywords
        try:
            obj = self.pageObj.findAll(attrs=param.METATAG['KEY'])
            if obj:
                self.metaDesc = obj[0]['content']
        except KeyError:
            pass

        try:
            self.title = self.pageObj.title.text
        except Exception:
            pass



    def __getPageObject(self):
        try:
            self.pageObj = BeautifulSoup(self.content, "lxml")
            self.__fill_details()
        except Exception as e:
            print 'Cannot create beatifulsoup object:',e

    def getOutLink(self):
        for link in self.pageObj.find_all('a'):
            print link.contents

    def getText(self):
        if not self.pageObj:
            self.__getPageObject()
        [s.extract() for s in self.pageObj(['style', 'script', '[document]', 'head'])]
        visible_text = self.pageObj.getText()
        return visible_text

    def _getSentences(self, text):
        sent = text.split('.')
        sent = filter(lambda s: s != '', sent)
        return self._cleanSent(sent)

    def _cleanSent(self, sent):
        clean = []
        for i in range(len(sent)):

            rawText = re.sub('[%s]' % string.punctuation,'',sent[i])
            rawText = re.sub('\d+','',sent[i])

            rawText = util.removeStopWords(rawText, param.STOPWORDS)
            clean.append(rawText)
        return clean

    def get_score(self, text):
        sentences = self._getSentences(text)
        for s in sentences:
            print s
        slen = len(sentences)
        score = [[0 for x in range(slen)] for x in range(slen)]
        
        for i in range(1, slen):
            if len(sentences[i])<15:
                continue
            j = 0
            while j<i:
                if len(sentences[j])<15:
                    j+=1
                    continue
                score[i][j] = util.compareSentences(sentences[i],sentences[j])
                score[j][i] = score[i][j]
                j+=1
        return sentences, score

    def get_top_match_sent(self, text, count=1):
        sent, score = self.get_score(text)
        slen = len(sent)
        score_dict = {}

        for i in range(slen):
            score_dict[sum(score[i])] = i

        top_sent = sorted(score_dict.keys(), reverse=True)

        for t in top_sent:
            print 'sent:', sent[score_dict[t]], ' score: ',t

        print 'Page Details:'
        print 'title:',self.title
        print 'Desc:',self.metaDesc
        print 'keywords:',self.metaKey



    def getKeywords(self):
        text = ''
        if self.pageObj:
            text = self.getText()
            text = util.removeStopWords(text, param.STOPWORDS)
            self.get_top_match_sent(text)
        