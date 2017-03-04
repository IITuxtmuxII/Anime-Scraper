from bs4 import BeautifulSoup
from Retrieve import retry_on_fail
import re
import requests
import urllib.request

class Nyaa(object):
    def __init__(self, url):
        self.url=url
        self.info_url=url + '?page=view&tid='
        self.dl_url=url + '?page=download&tid='

    @property
    def last_entry(self):
        r=retry_on_fail(requests.get, self.url)
        soup=BeautifulSoup(r.text, 'lxml')
        link=soup.find('tr', class_='tlistrow').find('td', class_='tlistname').a['href']
        return int(re.search('tid=([0-9]*)', link).group(1))


class NyaaEntry(object):
    def __init__(self, nyaa, nyaa_id):
        self.info_url='{}{}'.format(nyaa.info_url, nyaa_id)
        self.download_url='{}{}&magnet=1'.format(nyaa.dl_url, nyaa_id)
        self.nyaa_id='{}'.format(nyaa_id)

        r=retry_on_fail(requests.get, self.info_url)
        setattr(r, 'encoding', 'utf-8')
        self.page=BeautifulSoup(r.text, 'lxml')
        content=self.page.find('div', class_='content').text
        if 'The torrent you are looking for does not appear to be in the database' in content:
            #print('{}{} not exist...'.format(nyaa.info_url, nyaa_id))
            self.exists=False
        elif 'The torrent you are looking for has been deleted' in content:
            print(2)
            self.exists=False
        else:
            self.exists=True

    @property
    def category(self):
        return self.page.find('td', class_='viewcategory').find_all('a')[0].text

    @property
    def sub_category(self):
        return self.page.find('td', class_='viewcategory').find_all('a')[1].text

    @property
    def name(self):
        return self.page.find('td', class_='viewtorrentname').text

    @property
    def time(self):
        return self.page.find('td', class_='vtop').text.split(', ')

    @property
    def status(self):
        _status=self.page.find('div', class_=re.compile('content'))['class']
        if 'trusted' in _status:
            return 'trusted'
        elif 'remake' in _status:
            return 'remake'
        elif 'aplus' in _status:
            return 'a+'
        else:
            return 'normal'

    @property
    def tag(self):
        return str(self.page.find('div', class_='viewdescription'))[29:-6].rstrip().lstrip()

    @property
    def sld(self):
        viewtable=self.page.find('table', class_='viewtable')
        seeders=viewtable.find('span', class_='viewsn').text
        leechers=viewtable.find('span', class_='viewln').text
        downloads=viewtable.find('span', class_='viewdn').text
        return seeders, leechers, downloads

    @property
    def magnet(self):
        try:
            r=retry_on_fail(requests.head, self.download_url)
            if 'magnet' not in r:
                print('Aliased torrent, skipping...')
                return None
            return r
        except:
            return None
