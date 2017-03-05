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

Mode `new` resumes from the last retrieved id in the database.<br>
Mode `missed` mode rechecks for missed id not in the database.<br>
Mode `update` updates existing id and inserts missing id; slower than `missed` mode.<br>
Define start ID by appending the argument `--start=100`.<br>
<br>
Categories `categories.json` depicts categories to be indexed [modifying may corrupt existing databases].<br>
<br>
Modification of https://github.com/Hamuko/nyaamagnet
