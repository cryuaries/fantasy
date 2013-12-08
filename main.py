#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import jinja2
import os
from BeautifulSoup import BeautifulSoup

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class FantasyTable():
    def __init__(self, tablehead, theads, tbodys):
        self.tablehead = tablehead
        self.theads = theads
        self.tbodys = tbodys


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
        'mds' : "",
        'time_hour' : "",
        'time_minute' : "",
        'time_second' : "",
        'time_msec' : "",
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
    def post(self):
        template_values = {
        'mds' : "",
        'time' : "",
        'time_minute' : "",
        'time_second' : "",
        'time_msec' : "",
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class CloneHandler(webapp2.RequestHandler):
    def post(self):
        head = self.request.get("head") 
        body = self.request.get("body") 
        template = JINJA_ENVIRONMENT.get_template('fantasy.html')
        #self.response.write(template.render({'head': head[:-84], 'body': body}))
        #self.response.write(template.render({'head': head, 'body': "123"}))
        #self.response.write(body)
        #"""
        soup = BeautifulSoup(body)

        trs = soup.find('table', {"id" : "statTable1"}).findAll('tr')

        row = trs[1].findAll('div')
        #header = [ r.string for r in row]
        header = ['Rank', 'Team', 'GP', 'FG%', 'FT%', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']

        #self.response.write(header)
        #self.response.write("<br>")
        #col: Rank Team GP FG% FT% 3PTM PTS REB AST ST BLK TO
        name_col = 1
        average_overall_stats = []
        tbodys = []
        for i in range(2, 14):
            row = trs[i].findAll('td')
            stat = [ r.string for r in row]
            if row[4].a and str(row[4].a.string).endswith("*"):
                stat[4] = str(row[4].a.string)[:-1]
            stat[name_col] = row[name_col].a.string
            average_stat = ([int(x)/float(stat[2]) for x in stat[5:12]])    
            average_overall_stats.append(stat[:5]+average_stat)    
            row = stat[:5]+average_stat
            tbodys.append(row)
            #self.response.write(average_overall_stats[-1])
            #self.response.write("<br>")

        average_table = FantasyTable("Average Stats", header, tbodys)


        body1 = body[:body.find("<div id=\"roto-visualization\">")]
        body2 = body[body.find("<div id=\"roto-visualization\">"):]

        all_tables = [average_table]

        """
        # print all stats by rank
        for average_stat in average_overall_stats:
            self.response.write(average_stat[3:12] )
            self.response.write(average_stat[name_col])
            self.response.write("<br>")
        """

        # print average stats by rank
        for i in range(3, 12):
            #l = [[average_stat[1],average_stat[i]] for average_stat in average_overall_stats]
            if i != 11:
                average_overall_stats = sorted(average_overall_stats, key=lambda s: s[i], reverse=True)
            else:
                average_overall_stats = sorted(average_overall_stats, key=lambda s: s[i], reverse=False)
            #self.response.write(header[i])
            #self.response.write("<br>")
            thead = [header[i], "Team"]
            tbodys = []
            point = 12
            for j in average_overall_stats:
                row = [j[i], j[name_col]]
                #self.response.write(j[i])
                #self.response.write(j[name_col])
                #self.response.write("<br>")
                tbodys.append(row)
                j.append(point)
                point-=1
            all_tables.append(FantasyTable("Stat Rank", thead, tbodys))

        # print rank by player
        """
        for average_stat in average_overall_stats:
            thead = [average_stat[name_col], "Stat Rank"]
            #self.response.write(average_stat[name_col])
            tbodys = []
            #self.response.write("<br>")
            points = 0
            for i in range(3, 12):
                row = [header[i], average_stat[i+9]] 
                #self.response.write(header[i])
                #self.response.write(average_stat[i+9])
                #self.response.write("<br>")
                points += average_stat[i+9]
                tbodys.append(row) 
            average_stat.append(points)
            all_tables.append(FantasyTable("Stat Rank2", thead, tbodys))
            #self.response.write()
        #"""
        # print total rank
        # self.response.write("Total Ranks")
        # self.response.write("<br>")
        average_overall_stats = sorted(average_overall_stats, key=lambda s: s[-1], reverse=True)
        thead = ["Team", "Total Rank"] + header[3:12] 
        tbodys = []
        for j in average_overall_stats:
            row = [j[name_col], j[-1]] + j[12:21]
            tbodys.append(row)
            #self.response.write(j[name_col])
            #self.response.write(j[-1])
            #self.response.write(j[12:21])
            #self.response.write("<br>")
        all_tables.append(FantasyTable("Average Points", thead, tbodys))
        self.response.write(template.render({'head': head[:-84], 'body1': body1, 'body2': body2, 'tables': all_tables}))

class ConverterHandler(webapp2.RequestHandler):
    def post(self):
        template_values = {
        'mds' : "",
        'time' : "",
        'time_minute' : "",
        'time_second' : "",
        'time_msec' : "",
        }
        
        if "time" == self.request.get("from"):
            time_hour = int(self.request.get("time_hour"))
            time_minute = int(self.request.get("time_minute"))
            time_second = int(self.request.get("time_second"))
            time_msec = int(self.request.get("time_msec"))
            mds = (((time_hour * 60) + time_minute) * 60 + time_second) * 1000 + time_msec
        elif "mds" == self.request.get("from"):
            mds = self.request.get("mds")
            time = int(mds)
            time_msec = time % 1000
            time = time / 1000
            time_second = time % 60
            time = time / 60
            time_minute = time % 60
            time = time / 60
            time_hour = time
            
                
        template_values["mds"] = mds
        template_values["time_hour"] = time_hour
        template_values["time_minute"] = time_minute
        template_values["time_second"] = time_second
        template_values["time_msec"] = time_msec
    
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/converter', ConverterHandler),
    ('/clone', CloneHandler),
    ], debug=True)






