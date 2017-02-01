# to crawl every single url from one seed page
# this is the main example week3 lecture- How to build a search engine(2)

import urllib.request

def get_page(url):
    try:
        page_class = urllib.request.urlopen(url)
        page = page_class.read()
        return page
    except:
        return ''

def union(p,q):
    # given two list p ,q
    return list(set(p)|set(q))
     
            
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

url_seed = 'https://www.udacity.com/cs101x/index.html'
links = get_all_links(url_seed)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            crawled.append(page)
            tocrawl = union(tocrawl,get_all_links(page))
    return crawled

all_links = crawl_web(url_seed)
for link in all_links:
    print(link)

# def crawl_web(seed, max_depth):
    # tocrawl = [seed]
    # crawled = []
    # next_depth = []
    # depth = 0
    # while tocrawl and depth<=max_depth:
        # page = tocrawl.pop()
        # if page not in crawled:
            # union(next_depth, get_all_links(page))
            # crawled.append(page)
        # if not tocrawl:
            # tocrawl, next_depth = next_depth,[]
            # depth += 1
    # return crawled
# max_depth = 1
# print(crawl_web(url_seed,max_depth))
