import urllib.request

def get_page(url):
    try:
        page_class = urllib.request.urlopen(url)
        page = page_class.read()
        return page
    except:
        return ''

#print(page)
def get_next_target(page,search_index):
    # return hyperlink url, index of quote_end    
    search_index = page.find('<a href',search_index)
    if search_index == -1:
        return None,-1
    quote_start = page.find('"',search_index)
    quote_end = page.find('"',quote_start + 1)
    return page[quote_start + 1:quote_end], quote_end

def main(url):
    
    page = str(get_page(url))
    search_index = 0
    while True:
        url,search_index = get_next_target(page,search_index)        
        if url==None:
            break
        print(url)
        
#url = 'http://xkcd.com/353/'
url = 'https://www.udacity.com/cs101x/index.html'
main(url)
#url,index = get_next_target(page,search_index)