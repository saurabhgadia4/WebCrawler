import os
import logging
import subprocess
import shutil
import sys
from nltk.corpus import stopwords
import brightParam as param
from string import ascii_lowercase


SAMPLE_FILE = 'clean-file'
CORPUS_FILE = 'sample_test.txt'
CORPUS_WORDS = 'sample_word.txt'

cachedStopWords = stopwords.words("english")

def sentToWords():
# #1. splitting file by words
    try:
        shutil.copy2(SAMPLE_FILE, CORPUS_FILE)
        #truncExpr('\.', CORPUS_FILE, CORPUS_MINUS_SPACE)
        command = "tr -sc \'A-Za-z\.\' \'~\' < " + CORPUS_FILE + ">" + CORPUS_WORDS
        ret = subprocess.call(command, shell=True)
        if(ret):
            print "Error"
            sys.exit(-1)
        logging.info('successfully created word file')
        
        command = "sed -i \'s/~/~\\n/g\' " +  CORPUS_WORDS
        ret = subprocess.call(command, shell=True)
        if(ret):
            print "Error"
            sys.exit(-1)
        logging.info('successfully added space characters')

    except Exception as e:
        logging.exception(e)

def truncate(expr, inFile, outFile):
    try:
        command = "tr -d \'~\' < " + inFile + ">" + outFile
        ret = subprocess.call(command, shell=True)
        if(ret):
            print "Error"
            sys.exit(-1)
        logging.info('successfully added space characters')
    except Exception as e:
        logging.exception(e)

def removeStopWords(corpus, stopwords):
    stopwords = stopwords.split(',')
    parseList = [word for word in corpus.split() if word.lower() not in stopwords]
    return ' '.join(parseList)

def compareSentences(s1, s2):
    set_1 = set(s1.split(' '))
    set_2 = set(s2.split(' '))
    #print 'Inter: ',set_1.intersection(set_2)

    if len(set_1)==0 or len(set_2)==0:
        return 0
    return float(len(set_1.intersection(set_2)))/((len(set_1)+len(set_2))/2)


if __name__=="__main__":
    text = "I the am a doing saurabh"
    t = removeStopWords(text, param.STOPWORDS)
    print t