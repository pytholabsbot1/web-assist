import requests as req
import re,time,os
from bs4 import BeautifulSoup
import json
from PIL import Image

class webSearch:
    
    def __init__(self,query,num=10):
    
        self.res = req.get('https://www.google.co.in/search?q={}&num={}'.format(query,num))
        self.heads = [re.sub('<.*?>','',i.split('">')[-1][:-3]) for i in re.findall('<h3.*?>.*?</a',self.res.text)]
        self.urls = [i.split('q=')[1].split('&amp')[0] for i in re.findall('a href=\"/url\?q=http.*?\"',self.res.text)]
        self.urls = self.urls[abs(len(self.heads)-len(self.urls)) if(len(self.heads)!=len(self.urls)) else 0:]
        
        
class NewsSearch:
    
    def __init__(self,query,num=10):
    
        self.res = req.get('https://www.google.co.in/search?q={}&source=lnms&tbm=nws&num={}'.format(query,num))
        self.heads = [re.sub('<.*?>','',i.split('">')[-1][:-3]) for i in re.findall('<h3.*?>.*?</a',self.res.text)]
        self.urls = list(set([i.split('q=')[1].split('&amp')[0] for i in re.findall('a href=\"/url\?q=http.*?\"',self.res.text)]))
        self.urls = self.urls[abs(len(self.heads)-len(self.urls)) if(len(self.heads)!=len(self.urls)) else 0:]

        
        
class reverseImageSearch:
    def __init__(self,img_path):
        searchUrl = 'http://www.google.hr/searchbyimage/upload'
        multipart = {'encoded_image': (img_path, open(img_path, 'rb')), 'image_content': ''}
        imgurl = req.post(searchUrl, files=multipart, allow_redirects=False)
        
        
        self.res = req.get(imgurl.headers['Location'])
        self.heads = [re.sub('<.*?>','',i.split('">')[-1][:-3]) for i in re.findall('<h3.*?>.*?</a',self.res.text)]
        self.urls = [i.split('q=')[1].split('&amp')[0] for i in re.findall('a href=\"/url\?q=http.*?\"',self.res.text)]
        self.urls = self.urls[abs(len(self.heads)-len(self.urls)) if(len(self.heads)!=len(self.urls)) else 0:]
       
    
class imageSearch:
    def __init__(self,query):
        self.res = req.get('https://www.google.hr/search?q={}&source=lnms&tbm=isch'.format(query))
       
        def get_soup(url,header):
            return BeautifulSoup(req.get(url,headers=header).text,'html.parser')

        image_type="ActiOn"
        query= query.split()
        query='+'.join(query)
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        print(url)
        #add the directory for your image here
        DIR="Pictures"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = get_soup(url,header)


        self.imgs=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            self.imgs.append(link)

    def download(self,num=5,out_dir=os.getcwd(),fname=None):

        self.f_paths = []
        
        for i,url in enumerate(self.imgs):

            if(i==num):
                break

            r = req.get(url)
            ext = r.headers['Content-Type'].split('/')[1]
            path = os.path.join(out_dir,(fname if(fname) else '')+str(i)+'.'+ext)
            f = open(path, 'wb')
            for chunk in r.iter_content(chunk_size=512 * 1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    
            self.f_paths.append(path)


    def scale_all(self,basewidth=128):

        for img_path in self.f_paths:
            img = Image.open(img_path)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            img.save(img_path) 

        


#####----------------------------------------------------------------

base_path = os.getcwd()
file_dst = os.path.join(base_path,"downlaoded_files")


class Downloader:

    def __init__(self,url,filename):
        self.url = url
        self.filename = filename

        if(os.path.exists('downlaoded_files')==False):
            os.mkdir('downlaoded_files')
        
    def download(self):
       # NOTE the stream=True parameter


        def dwn(headers_ ,mode_):
            r = req.get(self.url, headers=headers_, stream=True)
            
            with open(os.path.join(file_dst,self.filename+'.'+ext), mode_) as f:
                for chunk in r.iter_content(chunk_size=1000): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            

        r = req.get(self.url, stream=True)
        
        ext = r.headers['Content-Type'].split('/')[-1].split(';')[0]
        filename = self.filename+'.'+ext
        
        
        if(os.path.exists(os.path.join(file_dst,filename))):

            print('appending to file --',filename)
            data = len(open(os.path.join(file_dst,filename),'rb').read())
            head = {"Range":"bytes={}-".format(data)}
            dwn(head ,'ab')

        else:
            print('creating a new file --',filename)
            dwn({},'wb')


###################



