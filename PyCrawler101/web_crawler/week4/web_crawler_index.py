# to crawl every single url from one seed page
# this is the main example of udacity Cs101, intro to computer, lesson4
import time
import urllib.request

def get_page(url):
    try:
        page_class = urllib.request.urlopen(url)
        page = (page_class.read())
        return page
    except:
        return ''

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
            
def get_next_target(page,search_index):
    search_index = page.find('<a href',search_index+1)
    if search_index==-1:
        return None,0
    quote_start = page.find('"',search_index+1)
    quote_end = page.find('"',quote_start+1) 
    url = page[quote_start+1:quote_end]
    return url,quote_end
    
def get_all_links(seed):
    page = str(get_page(seed))
    search_index = 0
    links = []
    while True:
        url,search_index = get_next_target(page,search_index)
        if url==None:
            break
        links.append(url)
    
    return links

seed = 'https://www.udacity.com/cs101x/index.html'

# Define a procedure, add_to_index,
# that takes 3 inputs:

# - an index: [[<keyword>,[<url>,...]],...]
# - a keyword: String
# - a url: String

# If the keyword is already
# in the index, add the url
# to the list of urls associated
# with that keyword.

# If the keyword is not in the index,
# add an entry to the index: [keyword,[url]]


index = []


def add_to_index(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            if not url in entry[1]:
                entry[1].append(url)
                return
    # not found, add new keyword to index
    index.append([keyword,[url]])

# Define a procedure, add_page_to_index,
# that takes three inputs:

#   - index
#   - url (String)
#   - content (String)

# It should update the index to include
# all of the word occurences found in the
# page content by adding the url to the
# word's associated url list.

def add_page_to_index(index,url,content):
    key_content = content.split()
    for keyword in key_content:
        add_to_index(index,keyword,url)

# lookup function:        
# - an index
# - keyword

# The procedure should return a list
# of the urls associated
# with the keyword. If the keyword
# is not in the index, the procedure
# should return an empty list.

#index = [['udacity', ['http://udacity.com', 'http://npr.org']],
#         ['computing', ['http://acm.org']]]

def lookup(index,keyword):
    for entry in index:
        if keyword == entry[0]:
            return entry[1]
    return []
#print(lookup(index,'udacity'))

# this is the main function to crawl web
def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        #print(tocrawl)
        page = tocrawl.pop()
        if page not in crawled:
            crawled.append(page)
            content = get_page(page)            
            add_page_to_index(index,page,content) # index with the format []
            union(tocrawl,get_all_links(page))
            
            #print(tocrawl)
        
    return index
start = time.clock()
index = crawl_web(seed)
runtime = time.clock() - start
print(runtime)