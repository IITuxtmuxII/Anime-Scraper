Nyaa Scraper
==========

# ABOUT
Scrape [nyaa](http://nyaa.se) and [sukebei](http://sukebei.nyaa.se).
- Index the id, category, subcategory, title and magnet.
- Incrementally index each torrent page, saving it to sqlite database file titled either `nyaa.sqlite` or `sukebei.sqlite`.
- [nyaa](http://nyaa.se) has over 903,600 torrent pages, a preindexed `nyaa,sqlite` database is included, use the `new` mode to update it.
- [sukebei](http://sukebei.nyaa.se) has over 2,256,000 torrent pages, a preindexed `sukebei,sqlite` database is planned to be included.

# REQUIREMENTS
- [Python 3](https://www.python.org/download/releases/3.0/)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [Requests](http://docs.python-requests.org/en/latest/)

# USAGE
- scraper.py nyaa|sukebei new|missed|update id
- Example: scraper.py nyaa

Parameter one: `nyaa` for http://nyaa.se or `sukebei` for http://sukebei.nyaa.se.
Parameter two: `new` (default) or `missed`, if excluded defaults to `new` mode.
Parameter three: Page number to start from, if excluded defaults to `1`.

- The `new` mode starts from the last retrieved id in the database.
- The `missed` rechecks for missed id not in the database.
- The `update` updates existing id and inserts missing id; slower than `missed` mode.

To start from a specific ID append the argument "--start=" followed by the page number
- Example: scraper.py nyaa --start=100

The `categories.json` file defines the categories to be indexed in the sqlite database, remove categories to exclude them from being added to the database. This should not be modified if there are existing databases as it will change them, it should only be changed for new databases.

# USAGE
This is an update for https://github.com/Hamuko/nyaamagnet which is no longer maintained.
