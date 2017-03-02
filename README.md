Anime Torrent Indexer
==========

Scrape [nyaa](http://nyaa.se), [sukebei](http://sukebei.nyaa.se), and [bakabt](http://nyaa.me).
- Saves data to sqlite database.
- As both ([nyaa](http://nyaa.se) 903,600 pages) and ([sukebei](http://sukebei.nyaa.se) 2,256,000 pages) have many pages to index, provided database files are *planned to be* included.

# REQUIREMENTS
- [Python 3](https://www.python.org/download/releases/3.0/)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [Requests](http://docs.python-requests.org/en/latest/)

# USAGE
- `Scraper.py nyaa|sukebei|bakabt new|missed|update`
- Example: `Scraper.py nyaa`

Parameter one: `nyaa` for http://nyaa.se or `sukebei` for http://sukebei.nyaa.se.<br>
Parameter two: `new` (default) or `missed`, if excluded defaults to `new` mode.<br>
Parameter three: Page number to start from, if excluded defaults to `1`.<br>

- The `new` mode starts from the last retrieved id in the database.
- The `missed` rechecks for missed id not in the database.
- The `update` updates existing id and inserts missing id; slower than `missed` mode.

To start from a specific ID append the argument "--start=" followed by the page number
- Example: `Scraper.py nyaa --start=100`

The `categories.json` file defines the categories to be indexed in the sqlite database, remove categories to exclude them from being added to the database. This should not be modified if there are existing databases as it will change them, it should only be changed for new databases.<br>
<br>
Modification of https://github.com/Hamuko/nyaamagnet which is no longer maintained.
