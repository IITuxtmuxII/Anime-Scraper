import mal_scraper
import time
import sys

from bs4 import BeautifulSoup
from Retrieve import retry_on_fail
import requests


class MAL(object):
    def __init__(self, url):
        self.url=url
        self.info_url=url + 'anime/'

    @property
    def last_entry(self):
        try:
            r=retry_on_fail(requests.get, self.url+'anime.php?o=9')
            soup=BeautifulSoup(r.text, 'lxml')
            seasonal = soup.find('div', class_='js-categories-seasonal')
            link = seasonal.findAll('tr')[1].find('td').a['href']
            if 'myanimelist.net/anime' in link:
                link = link.split('/')[4]
                return int(link)
            else:
                sys.exit('Failed retrieve last_entry')
        except:
            sys.exit('Failed retrieve last_entry')

class MALEntry(object):
    def __init__(self, mal, mal_id):
        self.info_url='{}{}'.format(mal.info_url, mal_id)
        self.mal_id='{}'.format(mal_id)
        self.maldata=""
        while not self.maldata:
            #print("Retrieve:",self.mal_id)
            retrievedata=mal_scraper.retrieve_anime(int(self.mal_id))
            if str(retrievedata) == "404":
                #print("Page not found",retrievedata)
                self.exists=False
                return None
            elif str(retrievedata) == "429":
                print("Too many requeusts...")
                time.sleep(2)
            else:
                self.maldata=retrievedata

        '''
        print(self.maldata[0]['success'])

        print(self.maldata[1])
        '''
        if self.maldata[0]['success'] == True:
            self.exists=True
        else:
            self.exists=False

    @property
    def name(self):
        name = self.maldata[1]['name']
        english = self.maldata[1]['name_english']
        japanese = self.maldata[1]['name_japanese']

        if name == None:
            name=""
        else:
            name=name.replace('|','')
        if english == None:
            english=""
        else:
            english=english.replace('|','')
        if name == english:
            english=""
        if japanese == None:
            japanese=""
        else:
            japanese=japanese.replace('|','')

        if name and not english and not japanese:
            title=str(name)
        elif name and english and not japanese:
            title=str(name)+' | '+str(english)
        else:
            title=str(name)+' | '+str(english)+' | '+str(japanese)
        return title

    @property
    def type(self):
        typex = self.maldata[1]['format']
        return typex

    @property
    def episodes(self):
        return self.maldata[1]['episodes']

    @property
    def aired_start(self):
        return self.maldata[1]['airing_started']

    @property
    def aired_end(self):
        return self.maldata[1]['airing_finished']

    @property
    def premiered(self):
        return self.maldata[1]['airing_premiere']

    @property
    def rating(self):
        return self.maldata[1]['rating']

    @property
    def published(self):
        return int(0)

    @property
    def status(self):
        return self.maldata[1]['airing_status']

    @property
    def category(self):
        return 'Anime'

    @property
    def sub_category(self):
        return self.maldata[1]['format']
