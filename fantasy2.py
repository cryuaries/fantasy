from BeautifulSoup import BeautifulSoup
import requests

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

req = requests.get(URLS['login'], headers=USERS, cookies=cookies)
cookies = dict(cookies.items() + req.cookies.items())
html = req.text
soup = BeautifulSoup(html)
glink = soup.find('div', id='gBtn').find('a', id='gBtnLnk')['href']
print glink
req = requests.get(glink, headers=USERS, cookies=cookies)
hidden_inputs = BeautifulSoup(req.text).find('form', id='gaia_loginform').findAll('input', attrs={'type':'hidden'})
data = dict(CREDS.items() + dict( (h.get('name'), h.get('value')) for h in hidden_inputs).items() )
cookies = dict(cookies.items() + req.cookies.items())
post_req = requests.post(URLS['post'], headers=USERS, cookies=cookies, data=data)
cookies = dict(cookies.items() + post_req.cookies.items())

# Handle redirect html 
html = post_req.text
soup = BeautifulSoup(html)
#br.open(soup.find('meta').get("content")[7:])
print soup.find('meta').get("content")[7:]
req = requests.get(soup.find('meta').get("content")[7:], headers=USERS, cookies=cookies)
cookies = dict(cookies.items() + req.cookies.items())

# Open my league standings
#br.open('http://basketball.fantasysports.yahoo.com/nba/53208/standings')
#req = requests.get(URLS['home'], headers=USERS, cookies=cookies)

#html = br.response().read()
"""
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