Anime Scraper
==========

Scrape [nyaa](http://nyaa.se), [sukebei](http://sukebei.nyaa.se), [bakabt](http://bakabt.me), and [myanimelist](https://myanimelist.net) data into sqlite database.

# REQUIREMENTS
- [Python 3](https://www.python.org/download/releases/3.0/)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [Requests](http://docs.python-requests.org/en/latest/)

# USAGE
- `Scraper.py nyaa|sukebei|bakabt|myanimelist new|missed|update`
- `Scraper.py nyaa update --start=100`

Mode `new` (default) resume from the last retrieved id in the database.<br>
Mode `missed` mode recheck missed id not in the database.<br>
Mode `update` update existing id, insert missed id; slower than `missed` mode.<br>
Argument `--start=100` define the id to start from.<br>
<br>
Categories `categories.json` depict categories to be indexed [modifying may corrupt existing database].

# FILES
Data is saved into the `sqlite` folder as `*.sqlite` file.

Note: myanimelist code uses a modified version of [mal_scraper](https://pypi.python.org/pypi/mal-scraper/0.1.0)
