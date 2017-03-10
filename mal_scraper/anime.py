import logging
from datetime import datetime
from bs4 import BeautifulSoup

from Retrieve import retry_on_fail
import requests
import re

from .consts import AiringStatus, Format
from .exceptions import MissingTagError, ParseError
from .mal_utils import get_date
from .requester import request_passthrough


logger = logging.getLogger(__name__)


def retrieve_anime(id_ref=1, requester=request_passthrough):
    """Return the metadata for a particular show.

    Args:
        id_ref (Optional(int)): Internal show identifier
        requester (Optional(requests-like)): HTTP request maker
            This allows us to control/limit/mock requests.

    Return:
        None if we failed to download the page, otherwise a tuple of two dicts
        (retrieval information, anime information).

        The retrieval information will include the keys:
            success (bool): Was *all* the information was retrieved?
                (Some keys from anime information may be missing otherwise.)
            scraper_retrieved_at (datetime): When the request was completed.
            id_ref (int): id_ref of this anime.
        The anime information will include the keys:
            See tests/mal_scraper/test_anime.py::test_download_first
    """
    url = get_url_from_id_ref(id_ref)
    #response = requester.get(url, headers = {'User-agent': 'test'}) # custom user agent to avoid 429 (too many requests) error
    response = retry_on_fail(requests.get, url)
    if not response:
        return 404
    if not response.ok:
        return response.status_code

    soup = BeautifulSoup(response.content, 'html.parser')
    success, info = _process_soup(soup)

    if not success:
        logger.warn('Failed to properly process the page "%s".', url)

    retrieval_info = {
        'success': success,
        'scraper_retrieved_at': datetime.utcnow(),
        'id_ref': id_ref,
    }

    return (retrieval_info, info)


def get_url_from_id_ref(id_ref):
    return 'http://myanimelist.net/anime/{:d}'.format(id_ref)


def _process_soup(soup):
    """Return (success?, metadata) from a soup of HTML.

    Returns:
        (success?, metadata) where success is only if there were zero errors.
    """
    retrieve = {
        'name': _get_name,
        'name_english': _get_english_name,
        'name_japanese': _get_japanese_name,
        'format': _get_format,
        'episodes': _get_episodes,
        'airing_status': _get_airing_status,
        'airing_started': _get_start_date,
        'airing_finished': _get_end_date,
        'airing_premiere': _get_airing_premiere,
        'rating': _get_rating,
    }

    retrieved = {}
    failed_tags = []
    for tag, func in retrieve.items():
        try:
            result = func(soup)
        except ParseError:
            logger.warn('Error processing tag "%s".', tag)
            failed_tags.append(tag)
            retrieved[tag] = None
        else:
            retrieved[tag] = result

    success = not bool(failed_tags)
    if not success:
        logger.warn('Failed to process tags: %s', failed_tags)

    return (success, retrieved)


def _get_name(soup):
    tag = soup.find('span', itemprop='name')
    if not tag:
        raise MissingTagError('name')

    text = tag.string
    return text


def _get_english_name(soup):
    pretag = soup.find('span', string='English:')
    if not pretag:
        return None
        #raise MissingTagError('english name')

    text = pretag.next_sibling.strip()
    return text


def _get_japanese_name(soup):
    pretag = soup.find('span', string='Japanese:')
    if not pretag:
        return None
        raise MissingTagError('japanese name')

    text = pretag.next_sibling.strip()
    return text

def _get_rating(soup):
    pretag = soup.find('span', string='Rating:')
    if not pretag:
        return None
        raise MissingTagError('rating')

    text = pretag.next_sibling.strip()
    return text

def _get_format(soup):
    pretag = soup.find('span', string='Type:')
    the_type = pretag.find_next('a').string.strip()
    if the_type not in ['TV','OVA','ONA','Special','Movie']: # cannot return None
        return 'TV'
    return the_type


def _get_episodes(soup):
    pretag = soup.find('span', string='Episodes:')
    if not pretag:
        raise MissingTagError('episodes')

    episodes_text = pretag.next_sibling.strip().lower()
    if episodes_text == 'unknown':
        return 0

    try:
        episodes_number = int(episodes_text)
    except (ValueError, TypeError):
        raise ParseError('episodes', 'Unable to convert text "%s" to int' % episodes_text)

    return episodes_number


def _get_airing_status(soup):
    pretag = soup.find('span', string='Status:')
    if not pretag:
        raise MissingTagError('status')

    status_text = pretag.next_sibling.strip().lower()
    status = {
        'finished airing': 'Finished Airing',
        'currently airing': 'Currently Airing',
        'not yet aired': 'Not yet aired',
    }.get(status_text, None)

    if not status:
        raise ParseError('status', 'Unable to identify text "%s"' % status_text)

    return status

def only_letters(string):
    return all(letter.isalpha() for letter in string)

def _get_start_date(soup):
    pretag = soup.find('span', string='Aired:')
    if not pretag:
        raise MissingTagError('aired')

    aired_text = pretag.next_sibling.strip()
    if aired_text == 'Not available':
        return None
    start_text = aired_text.split(' to ')[0]

    try:
        if only_letters(start_text.split(',')[0]):
            start_date = _get_date(start_text.split(',')[0]+' 1,'+start_text.split(',')[1])
        elif start_text.split(',')[0].isdigit():
            start_date = _get_date("Apr 1, " + str(start_text))
        else:
            start_date = _get_date(start_text)
        return start_date
    except ValueError as e:
        return None


def _get_end_date(soup):
    pretag = soup.find('span', string='Aired:')
    if not pretag:
        raise MissingTagError('aired')

    try:
        aired_text = pretag.next_sibling.strip()
        if ' to ' in aired_text:
            end_text = aired_text.split(' to ')[1]
            if end_text == '?':
                return None
            try:
                end_date = _get_date(end_text)
            except ValueError:
                return None
                #raise ParseError('airing end date', 'Cannot process text "%s"' % end_text)
            return end_date
    except ValueError as e:
        return None
    return None

def _get_date(date_text):
    return eval("get_date('"+date_text+"')")


def _get_airing_premiere(soup):
    pretag = soup.find('span', string='Premiered:')
    if not pretag:
        return None
        #raise MissingTagError('premiered')

    text = pretag.next_sibling.strip()
    if '?' in text:
        return None

    if 'add some' in str(pretag.find_next('a')):
        return None

    Months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month=0
    for i in Months:
        if i in str(pretag.find_next('a')):
            month=1
            break

    if month==1:
        try:
            season, year = pretag.find_next('a').string.lower().split(' ')
            if season == 'fall':
                season = 'autumn'
            elif season not in ('spring', 'summer', 'autumn', 'winter'):
                print('unknown season', pretag.find_next('a'))
                return None
                #raise ParseError('premiered', 'Unable to identify season "%s"' % season)

            try:
                year = int(year)
            except (ValueError, TypeError):
                print('unknown year', pretag.find_next('a'))
                return None
                #raise ParseError('premiered', 'Unable to identify year "%s"' % year)

            return (year, season)
        except:
            return None
    else:
        return None
