from __future__ import print_function
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)


# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]



URL  = 'https://login.yahoo.com/config/login?.src=spt&.intl=us&.lang=en-US&.done=http://basketball.fantasysports.yahoo.com/nba'
# The site we will navigate into, handling it's session
br.open(URL)

for l in br.links(text_regex='Google'):    
    br.follow_link(l)

br.select_form(nr=0)    
br["Email"] = "cryuaries@gmail.com"
br["Passwd"] = ""
br.submit()

    
# Handle redirect html 
html = br.response().read()
soup = BeautifulSoup(html)
br.open(soup.find('meta').get("content")[7:])

# Open my league standings
br.open('http://basketball.fantasysports.yahoo.com/nba/53208/standings')

html = br.response().read()
soup = BeautifulSoup(html)

trs = soup.find('table', {"id" : "statTable1"}).findAll('tr')

row = trs[1].findAll('div')
header = [ r.text for r in row]

vv = []
for i in range(2, 13):
    row = trs[i].findAll('td')
    v = [ r.text for r in row]
    v.extend([int(x)/float(v[2]) for x in v[5:12]])
    vv.append(v)    
    print(v)

# print all stats by rank
for v in vv:
    print(v[12:19], v[1])

# print average stats by rank
for i in range(12, 19):
    l = [[v[1],v[i]] for v in vv]
    l = sorted(l, key=lambda s: s[1], reverse=True)
    print(header[i-7])
    for k in l:
        print(k)
    print()
