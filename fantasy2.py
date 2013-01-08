# http://utilitymill.com/help#imports

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import cookielib

CREDS = {'Email': 'cryuaries@gmail.com',                                             
         'Passwd': 'topplayer'}                                            
URLS = {'login': 'https://login.yahoo.com/config/login?.src=spt&.intl=us&.lang=en-US&.done=http://basketball.fantasysports.yahoo.com/nba',
        'post': 'https://accounts.google.com/ServiceLoginAuth',                   
        'home': 'http://basketball.fantasysports.yahoo.com/nba/53208/standings'}

USERS = { 'User-agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1',          
          'Accept-Encoding' : 'gzip, deflate',
          'Connection' : 'keep-alive'}

cookies = {'B':'8k6i9lp8eisn6'}

html = ""

redirect_headers = ""

def get_cookies_header(cookies):
    s = ""
    for key, value in cookies.items(): 
        s = s + key + "=" + value + "; "
    if s[-2:] == "; ":
        s = s[:-2]
    return s

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):        
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)              
        result.status = code                                 
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):
        redirect_headers = fp.headers        
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        result.headers = redirect_headers
        result.status = code                                
        return result               

def test():                                                                
    cookies = get_logged_in_cookies()                                      
    #req_with_logged_in_cookies = requests.get(URLS['home'], cookies=cookies)    
    #assert 'You are signed in' in req_with_logged_in_cookies.text
    #print "If you can see this message you must be logged in."

def get_logged_in_cookies2():                                               
    req = requests.get(URLS['login'])                                      
    hidden_inputs = BS(req.text).find('form', attrs={'name':'login_form'}).findAll('input', attrs={'type':'hidden'}) 
    data = dict(CREDS.items() + dict( (h.get('name'), h.get('value')) for h in hidden_inputs).items() ) 
    post_req = requests.post(URLS['post'], cookies=req.cookies, data=data) 
    return post_req.cookies          

def get_logged_in_cookies():                                               
    req = requests.get(URLS['login'], headers=USERS)                                    
    html = req.text
    #print html
    soup = BeautifulSoup(html)
    glink = soup.find('div', id='gBtn').find('a', id='gBtnLnk')['href']
    print glink
    cookies = req.cookies
    print cookies
    #req = requests.get(glink, cookies=req.cookies)
    #print req.text
    #data = dict(CREDS.items())
    #post_req = requests.post(URLS['post'], cookies=req.cookies, data=data) 
    #return post_req.cookies                                                

#test()

cj = cookielib.CookieJar()
c = cookielib.Cookie(None, 'B', cookies['B'], '80', '80', 'yahoo.com', 
       None, None, '/', None, False, False, '', None, None, None)
cj.set_cookie(c)
print c
req = urllib2.Request(URLS['login'])
req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
f = opener.open(req)

html = f.read()
soup = BeautifulSoup(html)
glink = soup.find('div', id='gBtn').find('a', id='gBtnLnk')['href']
print glink
req = urllib2.Request(glink)
req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
f = opener.open(req)
#print f.headers
#print f.read()
hidden_inputs = BeautifulSoup(f.read()).find('form', id='gaia_loginform').findAll('input', attrs={'type':'hidden'})
data = dict(CREDS.items() + dict( (h.get('name'), h.get('value')) for h in hidden_inputs).items() )
#cookies = dict(cookies.items() + req.cookies.items())
req = urllib2.Request(URLS['post'], urllib.urlencode(dict([k.encode('utf-8'),unicode(v).encode('utf-8')] for k,v in data.items())))
req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
f = opener.open(req)
# Handle redirect html 
html = f.read()
soup = BeautifulSoup(html)
#br.open(soup.find('meta').get("content")[7:])
print soup.find('meta').get("content")[7:]
#req = requests.get(soup.find('meta').get("content")[7:], headers=USERS, cookies=cookies)
#cookies = dict(cookies.items() + req.cookies.items())

req = urllib2.Request(soup.find('meta').get("content")[7:])
req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
req.add_header('Accept-Language', 'zh-tw,en-us;q=0.7,en;q=0.3')
req.add_header('Accept-Encoding', 'gzip, deflate')
req.add_header('Connection', 'keep-alive')

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), SmartRedirectHandler())
f = opener.open(req)
print f.headers
cc = f.headers['Set-Cookie']
cc.split(';')[0].split('Y=')[1]

# Open my league standings
#br.open('http://basketball.fantasysports.yahoo.com/nba/53208/standings')
#req = requests.get(URLS['home'], headers=USERS, cookies=cookies)
#print req.text
#Y=v=1&n=76r9dv6utqrn3&l=02530u3xr0s3041vv1tsutttwrqq003x/o&p=02ivvtw002000000&iz=&r=qh&lg=en-US&intl=us&np=1;

req = urllib2.Request(URLS['home'])
req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
req.add_header('Accept-Language', 'zh-tw,en-us;q=0.7,en;q=0.3')
#req.add_header('Accept-Encoding', 'gzip, deflate')
req.add_header('Connection', 'keep-alive')

f = opener.open(req)
html = f.read()

#"""
soup = BeautifulSoup(html)

trs = soup.find('table', {"id" : "statTable1"}).findAll('tr')

row = trs[1].findAll('div')
header = [ r.text for r in row]

#col: Rank Team GP FG% FT% 3PTM PTS REB AST ST BLK TO
name_col = 1
average_overall_stats = []
for i in range(2, 14):
    row = trs[i].findAll('td')
    stat = [ r.text for r in row]
    average_stat = ([int(x)/float(stat[2]) for x in stat[5:12]])    
    average_overall_stats.append(stat[:5]+average_stat)    
    print(average_overall_stats[-1])

# print all stats by rank
for average_stat in average_overall_stats:
    print(average_stat[3:12], average_stat[name_col])

# print average stats by rank
for i in range(3, 12):
    #l = [[average_stat[1],average_stat[i]] for average_stat in average_overall_stats]
    if i != 11:
        average_overall_stats = sorted(average_overall_stats, key=lambda s: s[i], reverse=True)
    else:
        average_overall_stats = sorted(average_overall_stats, key=lambda s: s[i], reverse=False)
    print(header[i])
    point = 12
    for j in average_overall_stats:
        print(j[i], j[name_col])
        j.append(point)
        point-=1
    print()
    
# print rank by player
for average_stat in average_overall_stats:
    print(average_stat[name_col])
    points = 0
    for i in range(3, 12):
        print(header[i], average_stat[i+9])
        points += average_stat[i+9]
    average_stat.append(points)
    print()

# print total rank
print("Total Ranks")
average_overall_stats = sorted(average_overall_stats, key=lambda s: s[-1], reverse=True)
for j in average_overall_stats:
    print(j[name_col], j[-1], j[12:21])
print()

#"""
