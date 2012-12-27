from __future__ import print_function
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

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
br["Passwd"] = raw_input("Input password for " + br["Email"] + ": ")
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
