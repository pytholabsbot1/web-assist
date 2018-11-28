import requests as req
import re,time,os

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
        self.imgs = [i.split('src="')[1].split('"')[0] for i in re.findall('<img.*?width=',self.res.text)]
    
    def download(self,out_dir=os.getcwd()):
        
        for i,url in enumerate(self.imgs):
            r = req.get(url)
            ext = r.headers['Content-Type'].split('/')[1]
            f = open(out_dir+'/'+str(i)+'.'+ext, 'wb')
            for chunk in r.iter_content(chunk_size=512 * 1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    

base_path = os.getcwd()
file_dst = base_path+"\\"+"downlaoded_files"


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
            
            with open(file_dst+"\\"+self.filename+'.'+ext, mode_) as f:
                for chunk in r.iter_content(chunk_size=1000): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            

        r = req.get(self.url, stream=True)
        
        ext = r.headers['Content-Type'].split('/')[-1].split(';')[0]
        filename = self.filename+'.'+ext
        
        
        if(os.path.exists(file_dst+"\\"+filename)):

            print('appending to file --',filename)
            data = len(open(file_dst+"\\"+filename,'rb').read())
            head = {"Range":"bytes={}-".format(data)}
            dwn(head ,'ab')

        else:
            print('creating a new file --',filename)
            dwn({},'wb')
