# web-assist
Tools for scraping and downloading internet resources 


Installation:
```
$ pip install web-assist 
```


# 1. Parse google search results

```
import webAssist as wb

res = wb.webSearch('hello',num=10)

## for headings
res.heads

##for result urls
res.urls
```

# 2. Download High quality images from google image search

```
import webAssist as wb

imgs = wb.imageSearch('dogs')

## for img urls
imgs.imgs

##download 2 images 
imgs.download(num='2')

##scale them according to basewidth
imgs.scale_all(128)
```

# 3.Parse google news 

```
import webAssist as wb

n = wb.NewsSearch('India',num=10)

## for headings
n.heads

##for urls
n.urls

```

# Download any file (resume supported) :

```
import webAssist as wb

d = wb.Downloader('url','filename')

## download

d.download()

```

