Anime Torrent Indexer
==========

Scrape [nyaa](http://nyaa.se), [sukebei](http://sukebei.nyaa.se), and [bakabt](http://bakabt.me) data into sqlite database.

# REQUIREMENTS
- [Python 3](https://www.python.org/download/releases/3.0/)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [Requests](http://docs.python-requests.org/en/latest/)

# USAGE
- `Scraper.py nyaa|sukebei|bakabt new|missed|update`
- `Scraper.py nyaa update --start=100`

Mode `new` (default) resume from the last retrieved id in the database.<br>
Mode `missed` mode recheck missed id not in the database.<br>
Mode `update` update existing id, insert missed id; slower than `missed` mode.<br>
Argument `--start=100` define the id to start from.<br>
<br>
Categories `categories.json` depict categories to be indexed [modifying may corrupt existing database].<br>
<br>
Modification of https://github.com/Hamuko/nyaamagnet
