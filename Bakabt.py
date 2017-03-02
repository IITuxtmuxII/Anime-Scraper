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
        self.pagen = str(page)

    def baka_list(self):
        page_index = {}
        page = self.url + "browse.php?page=" + self.pagen
        r = retry_on_fail(requests.get, page)
        setattr(r, 'encoding', 'utf-8')
        self.page = BeautifulSoup(r.text, "lxml")
        table = self.page.find("table", class_='torrents').find("tbody").find_all("tr")
        for tds in table:
            tdx=0
            for td in tds.find_all("td"):
                tdx+=1
                if len(tds)==5:
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

                        baka_id=self.baka_url_id
                        page_index[baka_id] = {}
                        page_index[baka_id]["baka_url"] = self.baka_url
                        page_index[baka_id]["category"] = self.category
                        page_index[baka_id]["title_orig"] = self.title_orig
                        page_index[baka_id]["title"] = self.title
                        page_index[baka_id]["resolution"] = self.resolution
                        page_index[baka_id]["sb"] = self.sb
                        page_index[baka_id]["cb"] = self.cb
                        page_index[baka_id]["tags"] = self.tags
                        page_index[baka_id]["added"] = self.added
                        page_index[baka_id]["size"] = self.size
                        page_index[baka_id]["downloads"] = self.downloads
                        page_index[baka_id]["seeders"] = self.seeders
                        page_index[baka_id]["leechers"] = self.leechers
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
            if "NoneType" not in str(e):
                print(e)
            return None

    @property
    def title(self):
        try:
            title=re.sub(r"[\(\[].*?[\)\]]", "", self.title_orig).rstrip().lstrip() # remove (), []
            if title.count('|') > 0:
                title_list=[]
                title_list.append(title.split('|')[0].lstrip().rstrip())
                title_list.append(title.split('|')[1].lstrip().rstrip()) # english
                if title.count('|') == 2:
                    title_list.append(title.split('|')[2].lstrip().rstrip()) # synonym
                return title_list
            else:
                return title
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
            return None

    @property
    def resolution(self):
        try:
            for tem in ["1080p","960p","720p","480p","360p","240p"]:
                if tem in self.title_orig:
                    return tem
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
    def dsl(self):
        try:
            if self.td5.text:
                return self.td5.text
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def downloads(self):
        try:
            if self.dsl.split('/')[0]:
                return self.dsl.split('/')[0]
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def seeders(self):
        try:
            if self.dsl.split('/')[1]:
                return self.dsl.split('/')[1]
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

    @property
    def leechers(self):
        try:
            if self.dsl.split('/')[2]:
                return self.dsl.split('/')[2]
            return None
        except AttributeError as e:
            if "NoneType" not in str(e):
                print(e)
        return None

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

    def quality(self):
        content = self.page.find('div', class_='content').text
        if 'Bad input' in content:
            self.exists = False
        else:
            if self.sub_category:
                return self.sub_category
            else:
                return None

    @property
    def sub_category(self):
        try:
            for list_item in self.page.find("div", class_='other-versions').find("ul").find_all("li"):
                for dic, tem in {"A":"A","B":"B","C":"C","D":"D"}.items():
                    if self.title in list_item.text:
                        #print("found",self.title)
                        if tem == list_item.find("span", class_="quality").text:
                            return tem
                        elif list_item.find("span", class_="quality").text == "": # unmoderated
                            return None
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
                self.get_torrent()
            elif "#" == link['href']:
                return None
            else:
                print("no link")
        return None

    @property
    def get_torrent(self):
        print(self.full_baka)
        r = retry_on_fail(requests.get, self.full_baka)
        if r.content:
            return r.content
        else:
            print("error torrent")
            return None
