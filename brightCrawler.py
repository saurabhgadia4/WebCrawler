from optparse import OptionParser
import brightParam as param
import brightPage
import urllib2

class Fetcher:
    def __init__(self, url, headers={}):
        self.url = url
        self.headers = headers

    def __request(self):
        try:
            request = urllib2.Request(self.url, headers=self.headers)
            handle = urllib2.build_opener()
        except Exception as e:
            print 'Unable to request for the url:',self.url
            print 'Error:',e.message
            return (None,None)
        return (request, handle)


    def fetch(self):
        req, handle = self.__request()
        content = ''
        if handle:
            try:
                content = unicode(handle.open(req).read(), "utf-8",
                                errors="replace")
            except urllib2.HTTPError, error:
                print 'Error: %s -> %s' % (error, self.url)
            except urllib2.URLError, error:
                print 'Error: %s -> %s' % (error, self.url)
        return content


if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ip",action="store", type="string", dest="input", help="specify input link to crawl")
    (options, args) = parser.parse_args()
    if options.input==None:
        print 'Program needs url as argument'
        print 'try --help for more option'
        exit()
    url = options.input
    fobj = Fetcher(url, headers={"User-Agent":param.USER_AGENT})
    content = fobj.fetch()
    page = brightPage.Page(url, content)
    page.getKeywords()
    



