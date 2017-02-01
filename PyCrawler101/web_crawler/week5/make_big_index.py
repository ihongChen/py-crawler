import time

def time_execution(code):
    start = time.clock()
    result = eval(code)
    run_time = time.clock()-start
    return result,run_time
    
def lookup(index,keyword):
    for entry in index:
        if keyword == entry[0]:
            return entry[1]
    return []


def add_to_index(index,keyword,url):     
    for entry in index:
        if keyword in entry[0]:
            if url not in entry[1]:
                entry[1].append(url)
                return
    index.append([keyword,[url]])
    
def make_string(p):
    s = ''
    for e in p:
        s = s + e
    return s
    
def make_big_index(size):
    index = []
    letters = ['a','a','a','a','a','a','a']
    while len(index) < size:
        word = make_string(letters)
        add_to_index(index,word,'fake')
        for i in range(len(letters)-1, 0,-1):
            if letters[i] < 'z':
                letters[i] = chr(ord(letters[i]) + 1)
                break
            else:
                letters[i] = 'a'
    return index

size = 10**4
indexSize = make_big_index(size)
print(time_execution("make_big_index(size)"))