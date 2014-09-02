from collections import deque
import urllib2
import urlparse
from cgi import escape
import re
from bs4 import BeautifulSoup
from Queue import Queue
import sys
import robotparser
import time


def convert_float(time_string):
    try:
        time = float(time_string)
    except:
        print"improper value"
        time = float("0")
    return time

def Extract_links(input_link):
    req_object = urllib2.Request(input_link)
    try:
        url_response = urllib2.urlopen(req_object)
        url_content = url_response.read()
        soup=BeautifulSoup(url_content)
        links_tags=soup.findAll('a',href=True)
    except urllib2.URLError, error:
        print sys.stderr, "error: %s" % error
        links_tags = []
    except urllib2.HTTPerror, error:
        if error.code == 404:
            print sys.stderr, "error : %s %s" %(error, error.url)
        else:
            print sys.stderr, "error: %s " % error
        link_tags = []
    return links_tags

def robots_standard(link , curr_link):
    robot_parser = robotparser.RobotFileParser()
    robot_parser.set_url(curr_link +"/robots.txt")
    robot_parser.read()
    print link.__str__()
    can_fetch_link = robot_parser.can_fetch(" * ", link)
    if can_fetch_link:
        return True
    else:
        return False

def filter_duplicates(tags_found, input_link):
    print "\n branch"
    print input_link
    print "\n"
    for tag in tags_found:
        href = tag.get("href")
        if href is not None:
            link = urlparse.urljoin(input_link, escape(href))
            #print link
            if link not in links_crawled and input_link in link:
            #if link not in links_crawled:
                bool_val = robots_standard(link, input_link)
                if bool_val and focused_crawl_flag != "y":
                    print link
                    links_queue.put(link)
                elif bool_val and focused_crawl_flag == "y":
                    if re.search(focus_regex, link, re.IGNORECASE):
                        links_queue.put(link)
                    print "not indexing "
    #wait = raw_input("press enter :")
    return;
        
print " program to crawl the web "
file_links = open("links_populate.txt", "w+")
focused_crawl_flag = raw_input( "do you want to perform a focused crawl y/n ? :" )

if focused_crawl_flag == "y" :
    focus_string = raw_input("focus_string :" )
else:
    focus_string = ""
focus_regex = r"[a-zA-Z0-9]*(" + re.escape(focus_string) + r")[a-zA-Z0-9]*"

input_link = raw_input("link : ")
crawl_time = convert_float(raw_input("crawl_delay: "))
print input_link

links_crawled=[]

links_crawled.append(input_link)
links_queue = Queue()


tags_found_first = Extract_links(input_link)
filter_duplicates(tags_found_first, input_link)


while not links_queue.empty():
    curr_link = links_queue.get()
    if curr_link not in links_crawled:
        time.sleep(crawl_time)
        links_extracted = Extract_links(curr_link)
        if links_extracted:
            links_crawled.append(curr_link)
            filter_duplicates(links_extracted, curr_link)
        else:
            print "no links from here"
    else:
        print "\nduplicate\n"

for link in links_crawled:
    file_links.write(link)
    file_links.write("\n")

    


    
    
    
    
