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

# Follows refresh 0 but not hangs on refresh > 0
#br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


URL  = 'https://login.yahoo.com/config/login?.src=spt&.intl=us&.lang=en-US&.done=http://basketball.fantasysports.yahoo.com/nba'
# The site we will navigate into, handling it's session
br.open(URL)
#print br.response().read()

# Show the available forms
"""
for f in br.forms():
    print f

Link(base_url='https://login.yahoo.com/config/login?.src=spt&.intl=us&.lang=en-US&.done=http://basketball.fantasysports.yahoo.com/nba', url='https://open.login.yahoo.com/openid/yrp/signin?idp=google&ts=1354699078&.intl=us&.lang=en%2dUS&.done=http%3A%2F%2Fbasketball.fantasysports.yahoo.com%2Fnba&rpcrumb=zR6d9T9AG3H&.src=spt', text='Google', tag='a', attrs=[('id', 'gBtnLnk'), ('href', 'https://open.login.yahoo.com/openid/yrp/signin?idp=google&ts=1354699078&.intl=us&.lang=en%2dUS&.done=http%3A%2F%2Fbasketball.fantasysports.yahoo.com%2Fnba&rpcrumb=zR6d9T9AG3H&.src=spt'), ('class', 'secondaryCta'), ('target', '_blank'), ('tabindex', '1')])
"""

for l in br.links(text_regex='Google'):    
    br.follow_link(l)

br.select_form(nr=0)    
br["Email"] = "cryuaries@gmail.com"
br["Passwd"] = "topplayer"
br.submit()

"""
for l in br.links():
    print l
    br.follow_link(l)"""
    
#br.open('http://basketball.fantasysports.yahoo.com/nba')
html = br.response().read()
soup = BeautifulSoup(html)
br.open(soup.find('meta').get("content")[7:])

br.open('http://basketball.fantasysports.yahoo.com/nba/53208/standings')

html = br.response().read()
soup = BeautifulSoup(html)
#soup.find('table', {"id" : "statTable1"})
#soup.find('table', {"id" : "statTable1"}).findAll('tr')[1] #header
#soup.find('table', {"id" : "statTable1"}).findAll('tr')[1].findAll('div')[0].string

trs = soup.find('table', {"id" : "statTable1"}).findAll('tr')

row = trs[1].findAll('div')
header = [ r.text for r in row]
print(header)

vv = []
for i in range(2, 13):
    row = trs[i].findAll('td')
    v = [ r.text for r in row]
    v.extend([int(x)/float(v[2]) for x in v[5:12]])
    vv.append(v)    
    print(v)


for v in vv:
    print(v[12:19], v[1])

for i in range(12, 20):
    l = [[v[1],v[i]] for v in vv]
    l = sorted(l, key=lambda s: s[1], reverse=True)
    print(header[i-7])
    for k in l:
        print(k)
    print()

"""
# Select the first (index zero) form
br.select_form(nr=0)

# User credentials
br.form['Email'] = 'cryuaries@gmail.com'
br.form['Passwd'] = 'topplayer'

# Login
br.submit()

# Filter all links to mail messages in the inbox
all_msg_links = [l for l in br.links(url_regex='\?v=c&th=')]
print br.response().read()
# Select the first 3 messages
for msg_link in all_msg_links[0:3]:
    print msg_link
    # Open each message
    #br.follow_link(msg_link)
    #html = br.response().read()
    #soup = BeautifulSoup(html)
    # Filter html to only show the message content
    #msg = str(soup.findAll('div', attrs={'class': 'msg'})[0])
    # Show raw message content
    #print msg
    # Convert html to text, easier to read but can fail if you have intl
    # chars
#   print html2text.html2text(msg)
    print
    # Go back to the Inbox
    #br.follow_link(text='Inbox')

# Logout
#br.follow_link(text='Sign out')
"""
