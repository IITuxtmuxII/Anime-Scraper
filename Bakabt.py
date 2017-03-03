from bs4 import BeautifulSoup
from Retrieve import retry_on_fail
import re
import requests
import sys
import time
import urllib.request
from urllib.parse import urlparse

class Baka(object):
    def __init__(self, url, page):
        self.url = str(url)
        self.pagen = str(page-1)

    def baka_list(self):
        page_index = {}
        page = self.url + "browse.php?page=" + self.pagen
        self.last_category=""
        print("> Index",page)
        r = retry_on_fail(requests.get, page)
        setattr(r, 'encoding', 'utf-8')
        self.page = BeautifulSoup(r.text, "lxml")
        table = self.page.find("table", class_='torrents').find("tbody").find_all("tr")
        for tds in table:
            tdx=0
            for td in tds.find_all("td"):
                append=False
                tdx+=1
                if len(tds)==5:
                    append=True
                    if tdx==1:
                        self.td1=td
                    if tdx==2:
                        self.td2=td
                    elif tdx==3:
                        self.td3=td
                    elif tdx==4:
                        self.td4=td
                    elif tdx==5:
                        self.td5=td
                elif len(tds)==4 and "Alternative versions" not in tds.text:
                    append=True
                    if tdx==1:
                        self.td2=td
                    if tdx==2:
                        self.td3=td
                    elif tdx==3:
                        self.td4=td
                    elif tdx==4:
                        self.td5=td
                if append==True:
                    if len(tds)==5 and tdx==5 or len(tds)==4 and tdx==4:
                        baka_id=self.baka_url_id
                        page_index[baka_id] = {}
                        page_index[baka_id]["baka_url_id"] = self.baka_url_id
                        page_index[baka_id]["baka_url"] = self.baka_url
                        if len(tds)==5:
                            page_index[baka_id]["category"] = self.category
                        elif len(tds)==4:
                            page_index[baka_id]["category"] = self.last_category
                        page_index[baka_id]["title_orig"] = self.title_orig
                        page_index[baka_id]["title"] = self.title
                        page_index[baka_id]["resolution"] = self.resolution
                        page_index[baka_id]["sb"] = str(self.sb)
                        page_index[baka_id]["cb"] = str(self.cb)
                        page_index[baka_id]["tags"] = str(self.tags)
                        page_index[baka_id]["added"] = self.added
                        page_index[baka_id]["size"] = self.size
                        page_index[baka_id]["sld"] = str(self.sld)
        return page_index

    @property
    def baka_url(self):
        try:
            if self.url+self.td2.a['href']:
                return self.url+self.td2.a['href']
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        except TypeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def baka_url_id(self):
        try:
            if int(urlparse(self.baka_url).path.split('/')[2]):
                return int(urlparse(self.baka_url).path.split('/')[2])
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def category(self):
        try:
            for dic, tem in {"series":"Anime Series","movie":"Anime Movie","ova":"OVA","ost":"Soundtrack","liveaction":"Live Action","musicvideo":"Music Video","lightnovel":"Light Novel","artbook":"Artbook","manga":"Manga"}.items():
                if tem in str(self.td1):
                    self.last_category=tem
                    return tem
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def title_orig(self):
        try:
            if self.td2.find('a', class_='title').text:
                return self.td2.find('a', class_='title').text
            return None
        except AttributeError as e:
            if self.td2.find('a', class_='alt_title').text:
                return self.td2.find('a', class_='alt_title').text
            elif "NoneType" not in str(e):
                print(e)
        return None

    @property
    def title(self):
        try:
            return re.sub(r"[\(\[].*?[\)\]]", "", self.title_orig).rstrip().lstrip() # remove (), []
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
            return None
        except TypeError:
            exit("title error")

    @property
    def resolution(self):
        try:
            for tem in ["1080p","960p","720p","480p","360p","240p"]:
                if tem in self.title_orig:
                    return tem
            return None
        except AttributeError as e:
            print(e)
        except TypeError as e:
            print(e)
        return None

    @property
    def sb(self):
        try:
            if str(re.match(r"[^[]*\[([^]]*)\]", self.title_orig).groups()):
                return str(re.match(r"[^[]*\[([^]]*)\]", self.title_orig).groups())
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def cb(self):
        try:
            if str(re.match(r"[^[]*\(([^]]*)\)", self.title_orig).groups()):
                return str(re.match(r"[^[]*\(([^]]*)\)", self.title_orig).groups())
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def tags(self):
        try:
            typex=[]
            for dic, tem in {"Blu-ray":"Blu-ray","Blu-ray":"BD","DVD":"DVD","SD":"SD","Web":"Web","FLAC":"FLAC","PDF":"PDF","MP3":"MP3","Raw":"Raw","Dub":" dub","Dub":" Dub","Scan":"Scan","Lossless":"Lossless","HD":"High Definition","Incomplete":"Incomplete","Multiaudio":"Multiaudio"}.items():
                if tem in str(self.td2):
                    typex.append(dic)
            if typex:
                return typex
            return None
        except TypeError as e:
            print(e)
        return None

    @property
    def added(self):
        try:
            if self.td3.text.replace("'","20"):
                return self.td3.text.replace("'","20")
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def size(self):
        try:
            if self.td4.text:
                return self.td4.text
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def sld(self):
            if self.td5.text:
                sld = self.td5.text
                return sld.split('/')[1], sld.split('/')[2], sld.split('/')[0]

    def last_entry(url):
        baka_url=url+"browse.php"
        r = retry_on_fail(requests.get, baka_url)
        setattr(r, 'encoding', 'utf-8')
        page = BeautifulSoup(r.text, "lxml")
        pager = page.find('div', class_='pager')
        pages=[]
        for link in pager.find_all("a", href=True):
            if(int(re.sub('.*?([0-9]*)$',r'\1',link['href']))):
                pages.append(re.sub('.*?([0-9]*)$',r'\1',link['href']))
        return int(max(pages))


class BakaEntry(object):
    def __init__(self, baka_url, baka_title):
        self.baka_url=baka_url
        self.title=baka_title
        self.exists = True

        r = retry_on_fail(requests.get, self.baka_url)
        setattr(r, 'encoding', 'utf-8')
        self.page = BeautifulSoup(r.text, "lxml")

    def status(self):
        content = self.page.find('div', class_='content').text
        if 'Bad input' in content:
            self.exists = False
        else:
            if self.sub_category:
                return self.sub_category
            else:
                return "normal"

    @property
    def sub_category(self):
        try:
            for list_item in self.page.find("div", class_='other-versions').find("ul").find_all("li"):
                for tem in ["A","B","C","D"]:
                    if self.title in list_item.text:
                        #print("found",self.title)
                        if tem == list_item.find("span", class_="quality").text:
                            return tem
                        elif list_item.find("span", class_="quality").text == "": # unmoderated
                            return "normal"
                return "normal"
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        except TypeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    def torrent(self):
        for link in self.page.find_all('a', class_='download_link', href=True):
            if ".torrent" in link['href']:
                parsed_uri = urlparse(self.baka_url)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                self.full_baka = domain + link['href']
                r = retry_on_fail(requests.get, self.full_baka)
                if r.content:
                    torrent = r.content
                    return torrent
            elif "#" == link['href']:
                return None
            else:
                print("no link")
        return None
