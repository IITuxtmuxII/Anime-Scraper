Anime Torrent Indexer
==========

Scrape [nyaa](http://nyaa.se), [sukebei](http://sukebei.nyaa.se), and [bakabt](http://bakabt.me).

# REQUIREMENTS
- [Python 3](https://www.python.org/download/releases/3.0/)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [Requests](http://docs.python-requests.org/en/latest/)

# USAGE
- `Scraper.py nyaa|sukebei|bakabt new|missed|update`
- Example: `Scraper.py nyaa`

The `new` mode starts from the last retrieved id in the database.<br>
The `missed` mode rechecks for missed id not in the database.<br>
The `update` mode updates existing id and inserts missing id; slower than `missed` mode.<br><br>

Argument: "--start=" followed by the ID number. Example: `Scraper.py nyaa --start=100`

The `categories.json` file defines the categories to be indexed in the sqlite database, remove categories to exclude them from being added to the database. This should not be modified if there are existing databases as it will change them, it should only be changed for new databases.<br>
<br>
Modification of https://github.com/Hamuko/nyaamagnet which is no longer maintained.
