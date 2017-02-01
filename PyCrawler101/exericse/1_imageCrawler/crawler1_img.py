import requests
from bs4 import BeautifulSoup  

url = 'http://pi.isuphoto.org/post/'

def save_image_from_crawler(url,pages):
    # input: url,page 
    # output: a set of image files save as pages' name
    for page in range(pages):
        img_no = '{}'.format(str(page+1))
        imgloc = url + img_no

        res = requests.get(imgloc)
        soup = BeautifulSoup(res.text)

        imge = soup.select('.postpic')
        try:
            postURL = imge[0].img.get('src')
            filename = img_no + '.jpg'
        
            with open(filename,'wb') as handle:
                resimg = requests.get(postURL)
                if not resimg.ok:
                    print 'OOPS, something wrong~'
                else:
                    for block in resimg.iter_content(1024):
                        handle.write(block)
                        
            print "pages {} is successfully saved in the disk".format(img_no)
        
        except IndexError:
            print "page number {} is not found.".format(img_no)