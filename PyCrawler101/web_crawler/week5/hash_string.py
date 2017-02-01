# Define a function, hash_string,
# that takes as inputs a keyword
# (string) and a number of buckets,
# and returns a number representing
# the bucket for that keyword.

def hash_string(keyword,buckets):
    val = 0
    for letter in keyword:
        val += ord(str(letter))
    return val%buckets

import urllib.request

def bad_hash_string(keyword,buckets):
    return (ord(str(keyword[0])))%buckets

def get_page(url):
    try:
        page_class = urllib.request.urlopen(url)
        page = page_class.read()
        return page
    except:
        return ''
        
def test_hash_function(func,keys,size):
    results = [0]*size 
    key_used = []
    for w in keys:
        if w not in key_used:
            hv = func(w,size)
            results[hv] += 1
            key_used.append(w)
    return results
   
contents = get_page('http://www.gutenberg.org/cache/epub/1661/pg1661.txt') # bytes
words = str(contents).split()
counts = test_hash_function(hash_string,words,100)

